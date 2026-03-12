# -*- coding: utf-8 -*-
import telepot
import os
import utils
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        return

    command = msg['text']
    print(f"Received command: {command}")

    if command == '/status':
        status = utils.get_account_status()
        response = f"📊 현재 계좌 상태\n총자산: {status['total_asset']:,}원\n수익률: {status['yield']}%"
    elif command == '/stop':
        response = "🚦 시스템 정지 명령을 확인했습니다. (기능 미구현)"
    else:
        response = "❓ 알 수 없는 명령입니다. (/status, /stop)"

    utils.send_telegram_message(response)

if __name__ == "__main__":
    bot = telepot.Bot(TOKEN)
    bot.message_loop(on_chat_message)
    print("📡 텔레그램 리스너 대기 중...")
    
    import time
    while True:
        time.sleep(10)
