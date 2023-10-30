# 부채비율이 200% 이상인 기업 제외하기

import pandas as pd
import datetime

class debt_ratio:
    def debt_ratio(self, year, q, y):
        # csv를 데이터프레임으로 저장하기
        df_jaemu = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_jaemu.csv', encoding='cp949')
        df_jaemu_y = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_jaemu_y.csv', encoding='cp949')
        
        # 필요없는 데이터 날리기
        df_jaemu = df_jaemu.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기말', '전전기말'], axis=1)
        df_jaemu_y = df_jaemu_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기말', '전전기말'], axis=1)
        
        if y == 'yes':
            return df_jaemu_y
        elif y == 'no':
            return df_jaemu
        
    def result_debt(self, y):
        ## 현재날짜 year:년도, q:분기, y: yes or no
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        
        # 연도 변수 선언
        year = nowDate[0:4]
        
        # 분기 계산하기 후 분기 변수 선언
        # 분기보고서 제출기한(1분기 : 1~3월, 3분기 : 7월~9월) = 분기 종료일로 부터 45일 이내
        # - 1분기 : 5월 15일
        # - 3분기 : 11월 15일
        # 반기보고서 제출기한(반기 : 1~6월) = 반기 종료일부터 45일 이내 
        # - 반기 : 8월 15일
        # 사업보고서 제출기한(1년 : 1월~12월) = 종료일 부터 90일 이내
        # - 사업 : 다음해 3월 31일까지
        if 331 <= int(nowDate[5:8]) < 515 :
            q = '4'
        elif 515 <= int(nowDate[5:8]) < 815:
            q = '1'
        elif 815 <= int(nowDate[5:8]) < 1115:
            q = '2'
        else:
            q = '3'
            
        jaemu_data = self.debt_ratio(year, q, 'no')
        jaemu_data_y = self.debt_ratio(year, q, 'yes')
        
        ## 자본총계 가져오기 : ifrs-full_Equity##
        # 1. 별도
        jaemu1 = jaemu_data[jaemu_data['항목코드'].isin(['ifrs-full_Equity'])]
        jaemu1.rename(columns={'당기 1분기말':'자본총계_당기1분기말'}, inplace=True)
        # 2. 연결
        jaemu1_y = jaemu_data[jaemu_data['항목코드'].isin(['ifrs-full_Equity'])]
        jaemu1_y.rename(columns={'당기 1분기말':'자본총계_당기1분기말(연결)'}, inplace=True)
        
        ## 부채총계 가져오기 : ifrs-full_Liabilities##
        jaemu2 = jaemu_data[jaemu_data['항목코드'].isin(['ifrs-full_Liabilities'])]
        jaemu2.rename(columns={'당기 1분기말':'부채총계_당기1분기말'}, inplace=True)
        jaemu2 = jaemu2.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        # 2. 연결
        jaemu2_y = jaemu_data[jaemu_data['항목코드'].isin(['ifrs-full_Liabilities'])]
        jaemu2_y.rename(columns={'당기 1분기말':'부채총계_당기1분기말(연결)'}, inplace=True)
        jaemu2_y = jaemu2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        ## 자본총계와 부채총계 합치기##
        jaemu = pd.merge(jaemu1,jaemu2,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu1_y,jaemu2_y,how='outer',on=['종목코드'])
        
        #print(jaemu)
        #print(jaemu_y)
        
        ## 부채율 구하기 ##
        # ,빼고 float으로 만들기
        jaemu.iloc[:,1:] = jaemu.iloc[:,1:].replace(',','',regex=True)
        jaemu_y.iloc[:,1:] = jaemu_y.iloc[:,1:].replace(',','',regex=True)
        
        # 전체를 numeric으로 변환하기
        a = 6
        row_count = len(jaemu.columns)
        exit = True
        
        while exit:
            jaemu.iloc[:,a] = pd.to_numeric(jaemu.iloc[:,a], downcast='float')
            jaemu_y.iloc[:,a] = pd.to_numeric(jaemu.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                exit = False
            
        
        # 부채율 = 자본총액 / 부채총액 * 100
        jaemu['debt'] = (jaemu['자본총계_당기1분기말'] / jaemu['부채총계_당기1분기말']) * 100
        jaemu_y['debt_y'] = (jaemu_y['자본총계_당기1분기말(연결)'] / jaemu_y['부채총계_당기1분기말(연결)']) * 100
        
        #print(jaemu)
        #print(jaemu_y)
        
        # 회전율(turnover) 3이하, 회수기간(term) 150일 이상은 부적정
        jaemu_name = []
        for i in jaemu.index:
            if jaemu.loc[i,'debt'] >= 200:
                jaemu_name.append(jaemu.loc[i,'회사명'])
                
        jaemu_name_y = []
        for i in jaemu_y.index:
            if jaemu_y.loc[i,'debt_y'] >= 200:
                jaemu_name_y.append(jaemu.loc[i,'회사명'])

        #print(jaemu_name)
        #print(jaemu_name_y) 
        
        if y == 'yes':
            return jaemu_name_y
        elif y == 'no':
            return jaemu_name
        
#debt_ratio().result_debt()
        
        