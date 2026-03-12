# -*- coding: utf-8 -*-

class RiskManager:
    def __init__(self):
        self.max_position_size = 0.1  # 단일 종목 최대 비중 10%
        self.stop_loss = -0.05        # 손절 라인 -5%
        self.take_profit = 0.15       # 익절 라인 +15%

    def can_trade(self, symbol):
        """리스크 관점에서 매매 가능 여부 판단"""
        # 실제 환경에서는 현재 포트폴리오 정보를 조회하여 판단
        # 샘플에서는 항상 True 반환
        return True

    def calculate_position(self, total_asset, risk_score):
        """자산 대비 투자 규모 계산"""
        base_size = total_asset * self.max_position_size
        # 리스크 점수에 따라 비중 조절 (점수가 높을수록 안정적)
        if risk_score > 90:
            return base_size
        elif risk_score > 80:
            return base_size * 0.7
        else:
            return base_size * 0.4
