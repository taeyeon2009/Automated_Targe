# -*- coding: utf-8 -*-
import requests
import config

def send_alert(message):
    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("텔레그램 설정이 없습니다.")
        return
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")
