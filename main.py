# -*- coding: utf-8 -*-
import pandas as pd
from data_loader import KISDataLoader
from indicator import TechnicalIndicator
from pattern_detector import PatternDetector
from filter import StockFilter
from scoring import Scorer
import telegram_alert
import config

def main():
    print("=== 한국 주식 세력주 탐지 시스템 시작 ===")
    loader = KISDataLoader()
    stocks = loader.get_stock_list_mini() # 분석 대상 종목
    
    results = []

    for symbol in stocks:
        print(f"[{symbol}] 분석 중...", end="\r")
        df = loader.fetch_ohlcv(symbol)
        if df is None: continue
        
        # 1. 지표 계산
        df = TechnicalIndicator.add_indicators(df)
        
        # 2. 필터링
        if not StockFilter.is_valid(df): continue
        
        # 3. 패턴 탐지
        is_breakout, b_high, b_low = PatternDetector.detect_box_range(df)
        is_converged = PatternDetector.detect_ma_convergence(df)
        vol_ratio = PatternDetector.detect_volume_spike(df)
        
        # 4. 스코어링
        score = Scorer.get_score(df, is_breakout, is_converged, vol_ratio)
        
        last = df.iloc[-1]
        results.append({
            "code": symbol,
            "name": f"종목({symbol})", # 실제로는 종목명 매핑 필요
            "price": int(last['close']),
            "score": score,
            "high": b_high
        })

    # 점수 기준 정렬
    top_stocks = sorted(results, key=lambda x: x['score'], reverse=True)[:5]

    if not top_stocks:
        print("\n조건에 맞는 종목이 없습니다.")
        return

    # 결과 출력 및 텔레그램 전송
    report = "🚀 *오늘의 폭등 전조 TOP 종목*\n\n"
    for s in top_stocks:
        reason = f"박스권 상단({s['high']}) 돌파 시도 중" if s['score'] > 70 else "매집 및 정배열 추세 양호"
        item_text = (
            f"📍 *{s['name']}* ({s['code']})\n"
            f"- 현재가: {s['price']:,}원\n"
            f"- *총점: {s['score']}점*\n"
            f"- 판단근거: {reason}\n"
            f"- 매수가: {s['price']:,}원 근처\n"
            f"- 손절가: {int(s['price'] * 0.93):,}원\n"
            f"- 목표가: {int(s['price'] * 1.2):,}원\n\n"
        )
        report += item_text
        print(f"[{s['score']}점] {s['name']} ({s['code']}) 탐지 완료")

    telegram_alert.send_alert(report)
    print("\n분석 완료 및 텔레그램 전송 성공!")

if __name__ == "__main__":
    main()
