# -*- coding: utf-8 -*-
import sys
import io

# Windows 터미널 출력 인코딩 강제 UTF-8 지정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import time
import schedule
from datetime import datetime
import pandas as pd
import utils
from risk_manager import RiskManager
from ai_hit_tracker import AIHitTracker

class AIQuantManager:
    def __init__(self):
        self.risk_manager = RiskManager()
        self.hit_tracker = AIHitTracker()
        self.is_running = False

    def check_market_opportunity(self):
        """시장 기회를 상시 분석합니다 (매 30분)"""
        now = datetime.now()
        print(f"[{now.strftime('%H:%M:%S')}] 시장 분석 중...")
        
        # 1. 시가총액 상위 종목 필터링
        top_stocks = utils.get_top_market_cap(limit=50)
        
        for stock in top_stocks:
            symbol = stock['symbol']
            name = stock['name']
            
            # 2. AI 분석 요청 (간소화된 로직)
            analysis = utils.get_ai_prediction(symbol)
            
            if analysis['signal'] == 'BUY' and analysis['score'] >= 80:
                # 3. 리스크 체크 및 타율 기록
                if self.risk_manager.can_trade(symbol):
                    msg = f"🚀 [AI 추천] {name}({symbol})\n"
                    msg += f"신호: {analysis['signal']} (점수: {analysis['score']})\n"
                    msg += f"이유: {analysis['reason']}\n"
                    msg += f"현재 타율: {self.hit_tracker.get_hit_rate():.1f}%"
                    
                    utils.send_telegram_message(msg)
                    self.hit_tracker.log_signal(
                        symbol, name, analysis['signal'], 
                        analysis['price'], analysis['score'], analysis['reason']
                    )

    def update_portfolio_status(self):
        """계좌 상태 및 타율 업데이트 (매 시간)"""
        status = utils.get_account_status()
        hit_rate = self.hit_tracker.get_hit_rate()
        
        msg = f"📊 [정기 보고]\n"
        msg += f"총 자산: {status['total_asset']:,}원\n"
        msg += f"수익률: {status['yield']:.2f}%\n"
        msg += f"AI 타율: {hit_rate:.1f}%"
        
        utils.send_telegram_message(msg)

    def run(self):
        print("🤖 AI 퀀트 매니저가 시작되었습니다.")
        utils.send_telegram_message("🤖 AI 퀀트 매니저 가동 시작!")
        
        # 스케줄 등록
        schedule.every(30).minutes.do(self.check_market_opportunity)
        schedule.every(1).hours.do(self.update_portfolio_status)
        
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    manager = AIQuantManager()
    manager.run()
