# 최고가 및 최저가 대비 주가위치 파악

import pandas as pd
import numpy as np

class juga_loca:
    def juga_loca(self):
        #df = pd.read_csv("onedaydata/3S/3S.csv", encoding='cp949')
        df = pd.read_csv("onedaydata/E1/E1.csv", encoding='cp949')
        data = df[['일자','종목코드', '종목명', '시가', '고가', '저가', '종가']]
        
        # n일 기준 최고가, 최저가 구하기
        num1 = data['일자'].count()
        n = 100
        num2 = num1-n
        data2 = data.loc[num2:num1,:]
        max_val = data2['고가'].max()
        min_val = data2['저가'].min()
        print(max_val)
        print(min_val)
        
        
        # 현재주가 구하기
        recent_price = data['종가'].iloc[-1]
        print(recent_price)
        
        # 최고가, 최저가 기준 현재주가 위치 구하기
        max_per_recent = recent_price / max_val * 100
        min_per_recent = (recent_price - min_val) / min_val * 100
        print(max_per_recent) # 최고가로부터 몇 % 수준인지
        print(min_per_recent) # 최저가로부터 몇 % 올랐는지