# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import os

class AIHitTracker:
    def __init__(self, log_file="ai_hits.csv"):
        self.log_file = log_file
        self._set_columns()

    def _set_columns(self):
        self.columns = [
            'timestamp', 'symbol', 'name', 'signal', 
            'price', 'ai_score', 'reason', 'hit'
        ]
        if not os.path.exists(self.log_file):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.log_file, index=False, encoding='utf-8-sig')

    def log_signal(self, symbol, name, signal, price, ai_score, reason):
        """AI의 예측 신호를 기록합니다."""
        new_row = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'symbol': symbol,
            'name': name,
            'signal': signal,
            'price': price,
            'ai_score': ai_score,
            'reason': reason,
            'hit': None  # 결과는 나중에 업데이트
        }
        df = pd.read_csv(self.log_file)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.log_file, index=False, encoding='utf-8-sig')

    def update_hits(self, current_prices):
        """예측 성공 여부(Hit)를 업데이트합니다."""
        df = pd.read_csv(self.log_file)
        
        for idx, row in df[df['hit'].isna()].iterrows():
            symbol = str(row['symbol']).zfill(6)
            if symbol in current_prices:
                current_price = current_prices[symbol]
                entry_price = row['price']
                
                # 매수 신호 시 1% 이상 상승하면 Hit
                if row['signal'] == 'BUY':
                    if current_price >= entry_price * 1.01:
                        df.at[idx, 'hit'] = True
                # 매도 신호 시 1% 이상 하락하면 Hit
                elif row['signal'] == 'SELL':
                    if current_price <= entry_price * 0.99:
                        df.at[idx, 'hit'] = True
                        
        df.to_csv(self.log_file, index=False, encoding='utf-8-sig')

    def get_hit_rate(self):
        """현재 타율(성공률)을 계산합니다."""
        df = pd.read_csv(self.log_file)
        # 결과가 판명된 데이터만 계산 (None 제외)
        processed = df.dropna(subset=['hit'])
        if len(processed) == 0:
            return 0.0
            
        successes = len(processed[processed['hit'] == True])
        return (successes / len(processed)) * 100
