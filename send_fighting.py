# -*- coding: utf-8 -*-
import sys
import io

# Windows 터미널 출력 인코딩 강제 UTF-8 지정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import utils

print("텔레그램으로 '화이팅' 메시지를 전송합니다...")
utils.send_telegram_message("화이팅")
print("전송 시도가 완료되었습니다.")
