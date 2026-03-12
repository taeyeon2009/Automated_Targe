import json
import urllib.request
import urllib.parse
import config

_kis_access_token = None

import requests

def send_telegram_message(message: str):
    """텔레그램 봇을 통해 지정된 채팅방으로 메시지를 전송합니다."""
    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("텔레그램 토큰 설정이 없습니다.")
        return
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        result = response.json()
        if not result.get("ok"):
            print(f"텔레그램 메시지 전송 실패: {result}")
    except Exception as e:
        print(f"텔레그램 메시지 전송 에러: {e}")

def init_kis_api() -> bool:
    """한국투자증권 API 접근 토큰(Access Token)을 발급받거나 갱신합니다."""
    global _kis_access_token
    if not config.KIS_APP_KEY or not config.KIS_APP_SECRET:
        print("한투 API 키가 설정되지 않았습니다.")
        return False
        
    url = f"{config.KIS_DOMAIN}/oauth2/tokenP"
    body = {
        "grant_type": "client_credentials",
        "appkey": config.KIS_APP_KEY,
        "appsecret": config.KIS_APP_SECRET
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            _kis_access_token = res.get("access_token")
            return True
    except Exception as e:
        print(f"한투 API 토큰 발급 실패: {e}")
        return False

def _get_kis_headers(tr_id: str) -> dict:
    return {
        "Content-Type": "application/json",
        "authorization": f"Bearer {_kis_access_token}",
        "appkey": config.KIS_APP_KEY,
        "appsecret": config.KIS_APP_SECRET,
        "tr_id": tr_id,
        "custtype": "P"
    }

def get_current_price(symbol: str) -> int:
    """특정 종목의 현재가를 조회합니다."""
    if not _kis_access_token:
        init_kis_api()
        
    url = f"{config.KIS_DOMAIN}/uapi/domestic-stock/v1/quotations/inquire-price"
    params = urllib.parse.urlencode({
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": symbol
    })
    full_url = f"{url}?{params}"
    
    req = urllib.request.Request(full_url, headers=_get_kis_headers("FHKST01010100"))
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if res.get("rt_cd") == "0":
                return int(res["output"]["stck_prpr"])
    except Exception as e:
        print(f"현재가 조회 실패 ({symbol}): {e}")
    return 0

def get_account_balance() -> dict:
    """현재 계좌 잔고 및 보유 종목을 조회합니다."""
    if not _kis_access_token:
        init_kis_api()
        
    # KIS_ACCOUNT_NO가 제대로 세팅되어 있어야 합니다 (예: 50000000-01)
    cano = config.KIS_ACCOUNT_NO.split("-")[0] if config.KIS_ACCOUNT_NO else ""
    acnt_prdt_cd = config.KIS_ACCOUNT_NO.split("-")[1] if config.KIS_ACCOUNT_NO and "-" in config.KIS_ACCOUNT_NO else "01"
    
    url = f"{config.KIS_DOMAIN}/uapi/domestic-stock/v1/trading/inquire-balance"
    params = urllib.parse.urlencode({
        "CANO": cano,
        "ACNT_PRDT_CD": acnt_prdt_cd,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "00",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "00",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    })
    full_url = f"{url}?{params}"
    
    # 모의투자용 계좌조회 TR_ID: VTTC8434R (실전 투자는 TTTC8434R)
    req = urllib.request.Request(full_url, headers=_get_kis_headers("VTTC8434R"))
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if res.get("rt_cd") == "0":
                return {
                    "balance": int(res["output2"][0]["dnca_tot_amt"]),
                    "positions": res["output1"]
                }
    except Exception as e:
        print(f"계좌 잔고 조회 실패: {e}")
    return {"balance": 0, "positions": []}

def send_order(symbol: str, order_type: str, qty: int, price: int = 0) -> dict:
    """한국투자증권 API를 통해 주식 매수/매도 주문 전송
    - order_type: 'BUY' 또는 'SELL'
    - price: 지정가 주문인 경우 가격, 시장가 주문인 경우 0
    """
    if not _kis_access_token:
        init_kis_api()
        
    url = f"{config.KIS_DOMAIN}/uapi/domestic-stock/v1/trading/order-cash"
    
    # 모의투자 기준 매수: VTTC0802U, 매도: VTTC0801U
    tr_id = "VTTC0802U" if order_type.upper() == "BUY" else "VTTC0801U"
    
    cano = config.KIS_ACCOUNT_NO.split("-")[0] if config.KIS_ACCOUNT_NO else ""
    acnt_prdt_cd = config.KIS_ACCOUNT_NO.split("-")[1] if config.KIS_ACCOUNT_NO and "-" in config.KIS_ACCOUNT_NO else "01"
    
    body = {
        "CANO": cano,
        "ACNT_PRDT_CD": acnt_prdt_cd,
        "PDNO": symbol,
        "ORD_DVSN": "00" if price > 0 else "01", # 00: 지정가, 01: 시장가
        "ORD_QTY": str(qty),
        "ORD_UNPR": str(price) if price > 0 else "0"
    }
    
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_get_kis_headers(tr_id))
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res
    except Exception as e:
        print(f"주문 전송 실패 ({symbol}): {e}")
        return {"rt_cd": "-1", "msg1": str(e)}

import os
import logging

def save_json(filepath: str, data: dict):
    """데이터를 JSON 파일로 저장합니다."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"JSON 저장 실패: {e}")

def load_json(filepath: str, default_data=None):
    """JSON 파일에서 데이터를 불러옵니다. 없으면 default_data 반환"""
    if default_data is None:
        default_data = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON 로드 실패: {e}")
    return default_data

def setup_logger(name: str) -> logging.Logger:
    """모듈별 특정 로거를 반환합니다."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        
        os.makedirs(config.LOG_DIR, exist_ok=True)
        fh = logging.FileHandler(os.path.join(config.LOG_DIR, f"{name}.log"), encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    return logger

def get_account_status() -> dict:
    """계좌의 현재 상태(총자산, 수익률 등)를 반환합니다."""
    balance_info = get_account_balance()
    # 실제 KIS 응답에 맞춰 계산 로직을 보강해야 하지만, 지금은 기본값을 반환하도록 구현합니다.
    total_asset = balance_info.get("balance", 0)
    # 수동/자동매매 시 수익률 계산 logic (임시 0.0)
    yield_rate = 0.0 
    
    return {
        "total_asset": total_asset,
        "yield": yield_rate,
        "positions": balance_info.get("positions", [])
    }

def get_top_market_cap(limit: int = 50) -> list:
    """시가총액 상위 종목 리스트를 가져옵니다. (현재는 설정된 종목 리스트 반환)"""
    # 실제 구현 시 KIS API의 '전종목시세' 등을 활용해야 하지만, 
    # 현재는 config에 설정된 종목들을 우선적으로 분석 대상으로 삼습니다.
    stocks = []
    for symbol in config.SYMBOL_LIST:
        stocks.append({"symbol": symbol, "name": f"종목({symbol})"})
    return stocks[:limit]

def get_ai_prediction(symbol: str) -> dict:
    """특정 종목에 대한 AI 예측 결과를 반환합니다."""
    current_price = get_current_price(symbol)
    
    # AI 분석 로직 (여기서는 테스트를 위해 랜덤/임시 점수를 생성합니다)
    import random
    score = random.randint(60, 95)
    signal = "BUY" if score >= 80 else "HOLD"
    
    return {
        "symbol": symbol,
        "price": current_price,
        "signal": signal,
        "score": score,
        "reason": "기술적 분석 지표 호전 (테스트 데이터)"
    }
