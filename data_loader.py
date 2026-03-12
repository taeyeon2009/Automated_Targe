# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
import time
import config

class KISDataLoader:
    def __init__(self):
        self.access_token = None
        self.issue_token()

    def issue_token(self):
        """API 접근 토큰 발급"""
        url = f"{config.KIS_DOMAIN}/oauth2/tokenP"
        headers = {"Content-Type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": config.KIS_APP_KEY,
            "appsecret": config.KIS_APP_SECRET
        }
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 200:
            self.access_token = res.json().get("access_token")
        else:
            print("토큰 발급 실패. config.py의 API 키를 확인하세요.")

    def get_headers(self, tr_id):
        return {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": config.KIS_APP_KEY,
            "appsecret": config.KIS_APP_SECRET,
            "tr_id": tr_id,
            "custtype": "P"
        }

    def fetch_ohlcv(self, symbol, count=100):
        """특정 종목의 일봉 데이터 조회 (OHLCV)"""
        url = f"{config.KIS_DOMAIN}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_PERIOD_DIV_CODE": "D",
            "FID_ORG_ADJ_PRC": "0000000001" # 수정주가 적용
        }
        
        res = requests.get(url, headers=self.get_headers("FHKST03010100"), params=params)
        time.sleep(0.05) # API 호출 제한 방지
        
        if res.status_code == 200:
            data = res.json().get("output2", [])
            if not data: return None
            
            df = pd.DataFrame(data)
            # 필요한 컬럼만 추출 및 타입 변환
            cols = {
                'stck_bsop_date': 'date',
                'stck_clpr': 'close',
                'stck_oprc': 'open',
                'stck_hgpr': 'high',
                'stck_lwpr': 'low',
                'acml_vol': 'volume'
            }
            df = df.rename(columns=cols)
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
            
            # 날짜순 정렬 (과거 -> 현재)
            df = df.sort_values(by='date').reset_index(drop=True)
            return df
        return None

    def get_stock_list_mini(self):
        """분석 대상 종목 리스트 (간이: 시가총액 상위 일부 등)"""
        # 실제로는 전종목 마스터 파일을 읽어야 하지만, 
        # API 테스트를 위해 config에 정의된 종목이나 코스피200 일부 종목 반환
        return ["005930", "000660", "035720", "035420", "005380", "068270", "207940", "005490", "051910", "032830"]
