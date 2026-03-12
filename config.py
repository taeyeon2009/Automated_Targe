# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드 (있을 경우)
load_dotenv()

# 한국투자증권 API 설정
KIS_APP_KEY = os.getenv("KIS_APP_KEY", "여기에_앱키_입력")
KIS_APP_SECRET = os.getenv("KIS_APP_SECRET", "여기에_시크릿_입력")
KIS_ACCOUNT_NO = os.getenv("KIS_ACCOUNT_NO", "계좌번호-01")
KIS_DOMAIN = "https://openapi.koreainvestment.com:9443"  # 실전투자: https://openapi.koreainvestment.com:9443

# 텔레그램 설정
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "여기에_토큰_입력")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "여기에_채팅ID_입력")

# 전략 설정값
SCAN_COUNT = 50           # 분석할 종목 수 (테스트용)
MIN_MARKET_CAP = 500      # 최소 시가총액 (억 단위, 예: 500억 이상)
MIN_VOLUME = 100000       # 최소 평균 거래량 (최근 20일 기준)
STRICT_FILTER = True      # 위험 종목(증100, 관리종목 등) 엄격 제외 여부

# 지표 가중치 (총합 100)
WEIGHT_VOLUME = 30        # 거래량/매집 점수 비중
WEIGHT_PATTERN = 30       # 박스권/돌파 패턴 비중
WEIGHT_TECHNICAL = 20     # MACD/RSI 등 지표 비중
WEIGHT_TREND = 20         # 이평선 정배열/수렴 비중
