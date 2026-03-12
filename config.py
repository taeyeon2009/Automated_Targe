import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 한국투자증권 API 설정
# 모의투자: https://openapivts.koreainvestment.com:29443
# 실전투자: https://openapi.koreainvestment.com:9443
KIS_DOMAIN = "https://openapivts.koreainvestment.com:29443"
KIS_APP_KEY = os.getenv("KIS_APP_KEY", "")
KIS_APP_SECRET = os.getenv("KIS_APP_SECRET", "")
KIS_ACCOUNT_NO = os.getenv("KIS_ACCOUNT_NO", "") # 예: 50000000-01

# 텔레그램 설정
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 전략 설정
SYMBOL_LIST = ["005930", "000660"] # 삼성전자, SK하이닉스
BUY_AMOUNT = 1000000 # 1회 매수 금액 (원)

# 기타 설정
LOG_DIR = "logs"
DATA_DIR = "data"
