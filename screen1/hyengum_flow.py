# 영업, 투자, 재무 현금흐름을 분석해서 투자에 부적정한 기업을 걸러내기
# 영업활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInOperatingActivities

# 투자활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInInvestingActivities

# 재무활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInFinancingActivities

import pandas as pd
import datetime

# 년도, 분기, 연결여부 별 데이터프레임 형성하기
class hyen_flow:
    def hyen_flow(self, year, q, y):
        # csv를 데이터프레임으로 저장하기
        df_hyen = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_hyen.csv', encoding='cp949')
        df_hyen_y = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_hyen_y.csv', encoding='cp949')
        
        # 필요없는 데이터 날리기
        df_hyen = df_hyen.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기 1분기', '전기', '전전기'], axis=1)
        df_hyen_y = df_hyen_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기 1분기', '전기','전전기'], axis=1)
        
        if y == 'yes':
            return df_hyen
        elif y == 'no':
            return df_hyen_y

    def result_flow(self):
        ## parameter에 년도, 분기, 연결여부 넣어서 데이터 가져오기
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
        
        print('현재년도 :', year, '현재분기 :', q)
        flow_data = self.hyen_flow(year,q,'yes')
        flow_data_y = self.hyen_flow(year,q,'no')
        #print(flow_data)
        #print(flow_data_y)
        
        
        
        ## 별도 현금흐름표에서 데이터가져오기
        ## 가져온 데이터에서 영업, 투자, 재무만 가져오기
        hyen1 = flow_data[flow_data['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1.rename(columns={'당기 1분기':'영업현금흐름_당기1분기'}, inplace=True)
                
        hyen2 = flow_data[flow_data['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2 = hyen2.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen2.rename(columns={'당기 1분기':'투자현금흐름_당기1분기'}, inplace=True)
                
        hyen3 = flow_data[flow_data['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3 = hyen3.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen3.rename(columns={'당기 1분기':'재무현금흐름_당기1분기'}, inplace=True)
            
        hyen = pd.merge(hyen1,hyen2, how='outer', on=['종목코드'])
        hyen = pd.merge(hyen,hyen3, how='outer', on=['종목코드'])
        hyen = hyen.drop_duplicates(['종목코드'])
        
        # 데이터의 ','를 제거하고 float 형식으로 바꾸기
        hyen.iloc[:,1:] = hyen.iloc[:,1:].replace(',','',regex=True)
        
        aa = 6
        row_count = len(hyen.columns)
        exit = True
                
        while exit:
            hyen.iloc[:,aa] = pd.to_numeric(hyen.iloc[:,aa], downcast='float')
            aa = aa + 1
            if aa == row_count:
                exit = False
        
        #print(hyen.dtypes)
        #print(hyen)
        
        
        
        ## 연결 현금흐름표에서 데이터가져오기
        ## 가져온 데이터에서 영업, 투자, 재무만 가져오기
        hyen1_y = flow_data_y[flow_data_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1_y.rename(columns={'당기 1분기':'영업현금흐름_당기1분기(연결)'}, inplace=True)
                
        hyen2_y = flow_data_y[flow_data_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2_y = hyen2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen2_y.rename(columns={'당기 1분기':'투자현금흐름_당기1분기(연결)'}, inplace=True)
                
        hyen3_y = flow_data_y[flow_data_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3_y = hyen3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen3_y.rename(columns={'당기 1분기':'재무현금흐름_당기1분기(연결)'}, inplace=True)
            
        hyen_y = pd.merge(hyen1_y,hyen2_y, how='outer', on=['종목코드'])
        hyen_y = pd.merge(hyen_y,hyen3_y, how='outer', on=['종목코드'])
        hyen_y = hyen_y.drop_duplicates(['종목코드'])
        
        # 데이터의 ','를 제거하고 float 형식으로 바꾸기
        hyen_y.iloc[:,1:] = hyen_y.iloc[:,1:].replace(',','',regex=True)
        
        bb = 6
        row_count = len(hyen_y.columns)
        exit = True
                
        while exit:
            hyen_y.iloc[:,bb] = pd.to_numeric(hyen_y.iloc[:,bb], downcast='float')
            bb = bb + 1
            if bb == row_count:
                exit = False
        
        #print(hyen_y.dtypes)
        #print(hyen_y)
        
        
        
        ## 별도 현금흐름표에서 위기종목 거르기
        # 영업 -, 투자 +, 재무 +
        # 영업 -, 투자 +, 재무 -
        flow_name = []
        for i in hyen.index:
            if hyen.loc[i,'영업현금흐름_당기1분기'] < 0: # 위기종목만 추출 => 위기종목만 제외하려면 >0 으로 교체
                if hyen.loc[i,'투자현금흐름_당기1분기'] > 0:
                    flow_name.append(hyen.loc[i,'회사명'])
        
        #print(flow_name)
        #print('별도현금흐름:',len(flow_name),'개')
        
        
        
        ## 연결 현금흐름표에서 위기종목 거르기
        # 영업 -, 투자 +, 재무 +
        # 영업 -, 투자 +, 재무 -
        flow_name_y = []
        for i in hyen_y.index:
            if hyen_y.loc[i,'영업현금흐름_당기1분기(연결)'] < 0: # 위기종목만 추출 => 위기종목만 제외하려면 >0 으로 교체
                if hyen_y.loc[i,'투자현금흐름_당기1분기(연결)'] > 0:
                    flow_name_y.append(hyen_y.loc[i,'회사명'])
        
        #print(flow_name_y)
        #print('연결현금흐름:',len(flow_name_y),'개')
        
        
        ## 별도와 연결이 같은 종목만 추출하기??
        
        ## 리턴값 입력하기 ##
        return flow_name_y
        #################