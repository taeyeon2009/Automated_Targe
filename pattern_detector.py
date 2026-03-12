# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class PatternDetector:
    @staticmethod
    def detect_box_range(df, window=20):
        """최근 N일간의 박스권 고가/저가 탐지"""
        recent = df.tail(window)
        high = recent['high'].max()
        low = recent['low'].min()
        current = df.iloc[-1]['close']
        
        # 현재가가 박스권 상단 5% 이내에 있는지 확인 (돌파 직전)
        is_near_breakout = (current >= high * 0.95) and (current <= high * 1.02)
        return is_near_breakout, high, low

    @staticmethod
    def detect_ma_convergence(df):
        """이동평균선 수렴도 측정 (5, 20, 60일선이 모여있는지)"""
        last = df.iloc[-1]
        ma_list = [last['ma5'], last['ma20'], last['ma60']]
        
        if any(np.isnan(ma_list)): return 0
        
        spread = (max(ma_list) - min(ma_list)) / min(ma_list)
        # 수렴도가 3% 이내면 에너지가 응축된 것으로 판단
        return 1 if spread < 0.03 else 0

    @staticmethod
    def detect_volume_spike(df):
        """평균 거래량 대비 갑작스러운 거래량 증가 탐지"""
        recent_vol = df.tail(5)['volume'].mean()
        avg_vol = df.tail(20)['volume'].mean()
        
        if avg_vol == 0: return 0
        
        ratio = recent_vol / avg_vol
        return ratio # 1.5배 이상이면 긍정적
