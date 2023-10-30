# 분산으로 변동성 파악하기
# 분산이란?
# = 확률변수가 기댓값으로부터 얼마나 떨어진 곳에 분포하는지를 가늠하는 숫자
# = (편차)^2 의 합 / 데이터의 개수
# 편차 = 평균과의 차이

import pandas as pd
import numpy as np

class var():
    def var(self):
        df = pd.read_csv("onedaydata/3S/3S.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/E1/E1.csv", encoding='cp949')
        
        # 분산을 구함
        # 현재가로 종가를 나누어서 분산을 비교할 수 있도록 만들어줌
        data = df[['일자','종목코드', '종목명', '시가', '고가', '저가', '종가']]
        recent_price = data['종가'].iloc[-1]
        data['분산'] = data['종가'] / recent_price
        jong_var1 = data['분산'].var() * 100
        jong_var1 = round(jong_var1,2)
        #print(data)
        print(jong_var1)
        
        # 기간에 따른 분산 구하기
        # 최근 n일 동안 분산구하기
        num1 = data['일자'].count()
        n = 100
        num2 = num1-n
        data2 = data.loc[num2:num1,:]
        jong_var2 = data2['분산'].var() * 100
        jong_var2 = round(jong_var2,2)
        print(jong_var2)