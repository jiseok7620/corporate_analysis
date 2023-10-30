# PER'' * EPS''로 예상 주가 구하기
'''
1. 기본PER, 기본EPS 구하기
 - PER : 주가 / EPS = 시가총액 / 순이익
 - EPS : 당기순이익 / 발행주식수
 
2. 적정PER, 적정EPS 구하기
 - 적정PER : 주가 / 적정EPS
 - 적정EPS : 적정당기순이익 / 적정발행주식수
 1) 당기순이익 => 예상순이익 계산
  : 당기순이익 + (현금흐름표상 꼭 더해주어야할 것) - (현금흐름표상 꼭 빼주어야할 것)
  : 당기순이익은 지배기업소유주지분 + 비지배지분 이므로
   당기순이익 = 당기순이익 - 비지배지분
 2) 발행주식수
  : 발행주식수 + (CB / 현재가) + (BW / 현재가)
  
3. 예상PER, 예상EPS 구하기
 - 예상PER = 적정PER * 가중치
  : 가중치 구하기
   1) 증가율! 무조건 증가율을 기준으로 업종을 구분해라!
     *영업이익률증가율, 순이익률증가율, 자산증가율
     *고성장, 성장, 보통, 퇴보, 고퇴보
 - 예상EPS = 적정EPS * 적정EPS평균증가율(분기기준 or 연기준) 
'''

import pandas as pd
import numpy as np

class per_eps:
    def per_eps(self):
        df = pd.read_csv("onedaydata/3S/3S.csv", encoding='cp949')
        #df = pd.read_csv("onedaydata/E1/E1.csv", encoding='cp949')
        data = df[['일자','종목코드', '종목명', '종가', '상장주식수']]
        #print(data)
        
        # 현재주가 구하기
        recent_price = data['종가'].iloc[-1]
        #print(recent_price)
        
        ### 해당 분기 당기순이익 구하기 ###
        df_posonik_y = pd.read_csv('report/2021_1_posonik_y.csv', encoding='cp949')
        df_posonik_y= df_posonik_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '당기 1분기 누적', '전기 1분기 3개월', '전기 1분기 누적', '전기', '전전기'], axis=1)
        posonik = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs-full_ProfitLoss'])]
        posonik.rename(columns={'당기 1분기 3개월':'당기순이익'}, inplace=True)
        dangi = posonik[posonik['회사명'] == 'E1']
        dangi.iloc[:,1:] = dangi.iloc[:,1:].replace(',','',regex=True)
        dangi.iloc[:,6] = pd.to_numeric(dangi.iloc[:,6], downcast='float')
        
        dangi_val = dangi['당기순이익'].values[0]
        #print(type(dangi))
        #print(type(dangi_val))
        #######################################################################
        
        # 발행주식수 구하기
        recent_jusik_su = data['상장주식수'].iloc[-1]
        #print(type(recent_jusik_su))
        
        # 기본 PER, EPS 구하기
        basic_EPS = dangi_val / recent_jusik_su
        basic_PER = recent_price / basic_EPS
        print('PER은? : ',basic_PER)
        print('EPS는? : ',basic_EPS)
        
        #########################################################################
        
        # 현금흐름표상 꼭 더해줄 것 구하기(감가상각비, 퇴직급여, 금융비용, 법인세비용)
        # 감가상각비 : dart_AdjustmentsForDepreciationExpense
        # 퇴직급여 : dart_AdjustmentsForProvisionForSeveranceIndemnities
        # 금융비용 : ifrs-full_AdjustmentsForFinanceCosts
        # 법인세비용 : ifrs-full_AdjustmentsForIncomeTaxExpense
        
        # 현금흐름표상 꼭 빼줄 것 구하기(지분법이익)
        
        # 당기순이익에서 비지배지분 빼주기
        posonik2 = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs-full_ProfitLossAttributableToNoncontrollingInterests'])]
        posonik2.rename(columns={'당기 1분기 3개월':'비지배지분'}, inplace=True)
        bigibae = posonik2[posonik2['회사명'] == 'E1']
        bigibae.iloc[:,1:] = bigibae.iloc[:,1:].replace(',','',regex=True)
        bigibae.iloc[:,6] = pd.to_numeric(bigibae.iloc[:,6], downcast='float')
        bigibae_val = bigibae['비지배지분'].values[0]
        print(bigibae_val)
        result = dangi_val - bigibae_val # 당기순이익 - 비지배지분이익
        print(result)
        
        # CB/현재가 구하기(전환사채[유동부채에서만] : dart_CurrentPortionOfConvertibleBonds - 재무상태표)
        df_jaemu_y = pd.read_csv('report/2021_1_jaemu_y.csv', encoding='cp949')
        df_jaemu_y = df_jaemu_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기말', '전전기말'], axis=1)
        jaemu1 = df_jaemu_y[df_jaemu_y['항목코드'].isin(['dart_CurrentPortionOfConvertibleBonds'])]
        jaemu1.rename(columns={'당기 1분기말':'전환사채'}, inplace=True)
        print(jaemu1)
        
        # BW/현재가 구하기(신주인수권부사채[유동부채에서만] : dart_CurrentPortionOfBondWithWarrant)
        jaemu2 = df_jaemu_y[df_jaemu_y['항목코드'].isin(['dart_CurrentPortionOfBondWithWarrant'])]
        jaemu2.rename(columns={'당기 1분기말':'신주인수권부사채'}, inplace=True)
        print(jaemu2)
        
        # 적정 PER, EPS 구하기
        
        ###########################################################################
        
        # 증가율을 이용해서 종목 분류 후 가중치 부여하기
        
        # EPS 평균증가율 구하기
        
        
        ####################################################################
        #리턴값을 입력하시오#
        
        ####################################################################