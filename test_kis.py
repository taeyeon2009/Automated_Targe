# -*- coding: utf-8 -*-
import sys
import io

# Windows 터미널 출력 인코딩 강제 UTF-8 지정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import utils

print("--- 한국투자증권 API 연결 테스트 ---")
status = utils.get_account_status()
print(f"연결 계좌 총자산: {status['total_asset']:,}원")
print("✅ API 연결 확인 완료!")
