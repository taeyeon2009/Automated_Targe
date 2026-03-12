# -*- coding: utf-8 -*-
import schedule
import time
import main
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def job():
    logger.info("정기 분석 작업을 시작합니다 (오전 9시)")
    try:
        main.main()
        logger.info("정기 분석 작업이 성공적으로 완료되었습니다.")
    except Exception as e:
        logger.error(f"분석 작업 중 오류 발생: {e}")

# 매일 오전 09:00에 실행 등록
schedule.every().day.at("09:00").do(job)

logger.info("=== 세력주 탐지 스케줄러가 시작되었습니다 ===")
logger.info("매일 오전 09:00에 분석 리포트를 전송합니다.")

while True:
    schedule.run_pending()
    time.sleep(60) # 1분마다 체크
