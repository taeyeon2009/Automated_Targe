# -*- coding: utf-8 -*-
import sys
import io

# Windows 터미널 출력 인코딩 강제 UTF-8 지정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import utils
utils.send_telegram_message("안녕")
