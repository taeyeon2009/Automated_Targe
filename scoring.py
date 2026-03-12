# -*- coding: utf-8 -*-
import config

class Scorer:
    @staticmethod
    def get_score(df, is_breakout, is_converged, vol_ratio):
        """각 지표를 가중치에 따라 점수화"""
        score = 0
        last = df.iloc[-1]
        
        # 1. 거래량/OBV (가중치 30)
        # OBV가 최근 5일간 계속 상승 추세인지 확인
        obv_trend = 1 if df['obv'].tail(5).is_monotonic_increasing else 0
        vol_score = (vol_ratio * 10) + (obv_trend * 10)
        score += min(vol_score, 1) * config.WEIGHT_VOLUME
        
        # 2. 패턴 (박스권/수렴) (가중치 30)
        pattern_score = (15 if is_breakout else 0) + (15 if is_converged else 0)
        score += (pattern_score / 30) * config.WEIGHT_PATTERN
        
        # 3. 기술지표 (RSI/MACD) (가중치 20)
        # RSI가 50~70 사이일 때 가장 이상적 (과열 전)
        tech_score = 0
        if 50 <= last['rsi'] <= 75: tech_score += 10
        if last['macd_hist'] > 0: tech_score += 10 # MACD 히스토그램 양수
        score += (tech_score / 20) * config.WEIGHT_TECHNICAL
        
        # 4. 추세 (이평 정배열 등) (가중치 20)
        trend_score = 0
        if last['ma5'] > last['ma20'] > last['ma60']: trend_score += 20
        score += (trend_score / 20) * config.WEIGHT_TREND
        
        return round(score, 1)
