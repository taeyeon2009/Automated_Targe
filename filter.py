# -*- coding: utf-8 -*-
import config

class StockFilter:
    @staticmethod
    def is_valid(df, info=None):
        """기본적인 필터링 (거래량, 시총 등)"""
        if df is None or len(df) < 60: return False
        
        last = df.iloc[-1]
        
        # 1. 거래량 필터 (최근 20일 평균 거래량이 기준치 미달이면 제외)
        avg_vol = df.tail(20)['volume'].mean()
        if avg_vol < config.MIN_VOLUME: return False
        
        # 2. 동전주 제외 (조절 가능)
        if last['close'] < 1000: return False
        
        # 3. 거래정지/급락주 제외 (당일 거래량이 거의 없거나 주가 변동이 비정상적일 때)
        if last['volume'] == 0: return False
        
        # TODO: 실제 운영시는 KIS API의 '종목 정보' 기능을 붙여 관리종목 체크 추가
        return True
