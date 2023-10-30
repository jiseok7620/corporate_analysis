# 거래량으로 유동성 파악

import pandas as pd
import numpy as np

class gurae:
    def gurae(self):
        df = pd.read_csv("onedaydata/3S/3S.csv", encoding='cp949')
        #print(data)
        
        data = df[['일자','종목코드', '종목명', '거래량', '거래대금']]
        #print(data2)
        
        ##############범위에 따른 n번째 최대, 최소값 구하기##################
        # 범위 설정하기
        start = 20200101
        end = 20210601
        data2 = data.loc[(data['일자'] > start)&(data['일자'] < end)]
        
        # 거래대금의 최대, 최소 구하기
        max_val = data2['거래대금'].max()
        min_val = data2['거래대금'].min()
        #print(max_val, min_val)
        
        # n번째로 큰 값 찾기
        subject = '거래대금'
        n = 0
        data2 = data2.sort_values(by=subject, ascending=False)
        data2 = data2.reset_index(drop=True)
        n_max_val = data2.loc[[n],:]
        print(n_max_val)
        
        # n번째로 작은 값 찾기
        subject = '거래대금'
        n = 0
        data2 = data2.sort_values(by=subject)
        data2 = data2.reset_index(drop=True)
        n_min_val = data2.loc[[n],:]
        print(n_min_val)

        
        ########################## 평균 구하기 ############################
        # 특정 범위 동안 평균구하기
        avg_val = data2['거래대금'].mean()
        print(avg_val)
        
        # 최근 n일 동안 평균구하기
        num1 = data['일자'].count()
        n = 20
        num2 = num1-n
        data3 = data.loc[num2:num1,:]
        n_avg_val = data3['거래대금'].mean()
        print(n_avg_val)
        
