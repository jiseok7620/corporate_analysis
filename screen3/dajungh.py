# 다중선형회귀분석을 이용한 예상주가 구하기
# 독립변수(x) : 거래량, 이평선과 종가의 이격도, 이평선간의 거리
# 종속변수(y) : 종가

import pandas as pd
import numpy as np

class dajungh:
    def dajungh(self):
        #df = pd.read_csv("onedaydata/3S/3S.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/E1/E1.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/KEC/KEC.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/KT/KT.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/LG/LG.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/NAVER/NAVER.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/POSCO/POSCO.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/S-Oil/S-Oil.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/SBS/SBS.csv", encoding='cp949')
        df = pd.read_csv("onedaydata/WISCOM/WISCOM.csv", encoding='cp949')
        data = df[['일자','종목코드', '종목명','저가', '고가', '종가', '거래량', '거래대금']]
        
        '''
        # 데이터를 n일 기간만 뽑아서 하기
        num1 = data['일자'].count()
        n = 500
        num2 = num1-n
        data = data.loc[num2:num1,:]
        '''
        
        # 10일, 20일, 60일, 120일 이동평균선 구하기
        data['10이평선'] = data['종가'].rolling(window=10).mean()
        data['20이평선'] = data['종가'].rolling(window=20).mean()
        data['60이평선'] = data['종가'].rolling(window=60).mean()
        data['120이평선'] = data['종가'].rolling(window=120).mean()
        print('데이터 : ', data)
        
        # 결측값이 있는 행 제거
        data = data.dropna(axis=0)
        data = data.reset_index(drop=True, inplace=False) # 인덱스 초기화
        
        # 종가 - 이동평균선(이동평균선과 종가 사이의 거리 구하기)
        # 0 이상 : 종가가 이동평균선 위에 있다.
        # 종가가 이동평균선 대비 몇 % 위에 있는지
        data['종가-20'] = ((data['종가'] - data['20이평선']) / data['종가']) * 100
        data['종가-60'] = ((data['종가'] - data['60이평선']) / data['종가']) * 100
        data['종가-120'] = ((data['종가'] - data['120이평선']) / data['종가']) * 100
        
        # 이동평균선 간의 거리구하기
        # 1. 20일과 60일선
        data['20-60'] = ((data['20이평선'] - data['60이평선']) / data['20이평선']) * 100
        # 2. 20일과 120일선
        data['20-120'] = ((data['20이평선'] - data['120이평선']) / data['20이평선']) * 100
        #print(data)
        
        #####################################################################
        # 종속변수 만들기 => 다음날 고가로 해보자
        imsi = data['고가']
        imsi = imsi.drop(imsi.index[0]) # 첫행삭제
        imsi = imsi.reset_index(drop=True, inplace=False) # 인덱스 초기화
        data['차일고가'] = imsi
        
        # 다음날 값을 예측하기위해 오늘의 종가, 거래량, 종가-이평거리, 20-60을 뽑자
        jong= data['종가'].iloc[-1]
        aa = data['종가'].iloc[-1]
        #bb = data['120이평선'].iloc[-1]
        cc = data['20-120'].iloc[-1]
        dd = data['거래대금'].iloc[-1]
        
        # 마지막 n개의 행 제거 -> 여기서는 마지막 행만
        data = data.drop(data.index[-1])
        print('데이터 : ', data)
        
        # 독립변수와 종속변수 지정
        x = data[['종가', '20-120', '거래대금']]
        y = data[['차일고가']] # => 종가를 n일 후 종가? 해튼 바꿔야됨
        ######################################################################
        
        # train, test로 분리하기
        from sklearn.model_selection import train_test_split # pip install scikit-learn
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, shuffle=True, random_state=34)
        
        ## 독립변수간의 다중공선성 확인 ##
        # 상관계수가 0.5 이상이면 다중공선성 의심
        x_train.corr()
        print('다중공선성 확인 : ', x_train.corr())
        
        # 분산팽창계수(VIF)가 10이상이면 다중공선성 의심(5를 기준으로 하기도 함)
        from statsmodels.stats.outliers_influence import variance_inflation_factor # pip install statsmodels
        vif = pd.DataFrame()
        vif['VIF_Factor'] = [variance_inflation_factor(x_train.values, i) for i in range(x_train.shape[1])]
        vif['Feature'] = x_train.columns
        vif.sort_values(by='VIF_Factor', ascending=True)
        print('분산팽창계수 : ', vif.sort_values(by='VIF_Factor', ascending=True))
        ################################
        
        ## OLS검정 ##
        # R-squared 확인 : 결정개수 확인(1이 100%)
        # => 0.7 이상이면 괜춘
        # 모형에 대한 p-value 확인(Prob(F-statistics)) : 0.05보다 작은지 확인
        # 각 독립변수의 계수에 대한 p-value(P>|t|) : 0.05보다 작은지 확인
        import statsmodels.api as sm
        x_train_1 = sm.add_constant(x_train, has_constant = "add")
        OLS_model = sm.OLS(y_train, x_train_1)
        fit_model = OLS_model.fit()
        fit_model.summary()
        print('OLS검점 : ', fit_model.summary())
        ##############
        
        '''
        # 데이터 정규화
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.fit_transform(x_test)
        y_train = scaler.fit_transform(y_train)
        y_test = scaler.fit_transform(y_test)
        '''
        
        # 모델 생성하기
        from sklearn.linear_model import LinearRegression
        mlr = LinearRegression()
        mlr.fit(x_train, y_train)
        
        # 모델의 정확도 평가 => 결정계수 R^2 값을 확인(1이 100%)
        mlr.score(x_train, y_train)
        print('모델의 정확도 평가 : ', mlr.score(x_train, y_train))
        
        ########################################
        # 독립변수 값 넣어주기 => 예측결과 확인
        insert_data = [[aa, cc, dd]]
        my_predict = mlr.predict(insert_data)
        print('종가 : ', jong)
        print('다음날 고가 예측 : ', my_predict)
        ########################################


        ####################################################################
        #리턴값을 입력하시오#
        
        ####################################################################