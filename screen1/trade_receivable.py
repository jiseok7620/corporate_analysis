#####################################
# 매출액에 비해 매출채권이 지나치게 높은기업 거르기
# 매출액 -> 포괄손익계산서 상 매출액
# 매출채권 -> 재무상태표 내 유동자산의 매출채권

# 매출채권회전율 = 매출액 / 매출채권
# 매출채권회수기간 = 365 / 매출채권회전율

# 매출채권 = (기초 매출채권 + 기말매출채권) / 2

# 매출채권회수기간은 5개월 이내가 적정 = 150일
# 매출채권 회전율은 4이상이 적정
#####################################

import pandas as pd
import datetime


# 년도, 분기, 연결여부 별 데이터프레임 형성하기
class trade_receivable:
    def trade_receivable_posonik(self, year, q, y):
        # csv를 데이터프레임으로 저장하기
        df_posonik = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_posonik.csv', encoding='cp949')
        df_posonik_y = pd.read_csv('D:/report_csv/report/'+year+'_'+q+'_posonik_y.csv', encoding='cp949')
        
        # 필요없는 데이터 날리기
        df_posonik = df_posonik.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '당기 1분기 누적', '전기 1분기 3개월', '전기 1분기 누적', '전기', '전전기'], axis=1)
        df_posonik_y = df_posonik_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '당기 1분기 누적', '전기 1분기 3개월', '전기 1분기 누적', '전기', '전전기'], axis=1)
        
        if y == 'yes':
            return df_posonik_y
        elif y == 'no':
            return df_posonik
        
        
    def trade_receivable_jaemu(self, year, q, y):
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
        
        
    def result_receivable(self):
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
        
        print('여기는 trade_receivable..','현재년도 :', year, '현재분기 :', q)
        posonik_data = self.trade_receivable_posonik(year,q,'no')
        posonik_data_y = self.trade_receivable_posonik(year,q,'yes')
        jaemu_data = self.trade_receivable_jaemu(year, q, 'no')
        jaemu_data_y = self.trade_receivable_jaemu(year, q, 'yes')
        # 재무상태표는 1년전꺼도 표시
        year_ago = str(int(year) - 1)
        #print(year_ago)
        jaemu_data_ago = self.trade_receivable_jaemu(year_ago, q, 'no')
        jaemu_data_y_ago = self.trade_receivable_jaemu(year_ago, q, 'yes')
        #print(posonik_data)
        #print(posonik_data_y)
        #print(jaemu_data)
        #print(jaemu_data_y)
        
        
        ## 포괄손익계산서와 재무상태표에서 필요한 데이터만 가져오기
        # 포괄손익계산서에서 매출액 가져오기
        # 1. 별도
        posonik1 = posonik_data[posonik_data['항목코드'].isin(['ifrs-full_Revenue'])]
        posonik1.rename(columns={'당기 1분기 3개월':'(포)매출액_당기1분기3개월'}, inplace=True)
        # 2. 연결
        posonik1_y = posonik_data_y[posonik_data_y['항목코드'].isin(['ifrs-full_Revenue'])]
        posonik1_y.rename(columns={'당기 1분기 3개월':'(포)매출액_당기1분기3개월(연결)'}, inplace=True)
        
        # 재무상태표에서 매출채권 가져오기
        # 당년 + 작년 / 2
        # 1. 별도
        jaemu1 = jaemu_data[jaemu_data['항목코드'].isin(['dart_ShortTermTradeReceivable', 'ifrs-full_TradeAndOtherCurrentReceivables'])]
        jaemu1.rename(columns={'당기 1분기말':'매출채권_당기1분기말'}, inplace=True)
        jaemu1 = jaemu1.drop_duplicates(['종목코드'], keep='last') # 중목 중 마지막 행 제거
        # 2. 연결
        jaemu1_y = jaemu_data[jaemu_data['항목코드'].isin(['dart_ShortTermTradeReceivable', 'ifrs-full_TradeAndOtherCurrentReceivables'])]
        jaemu1_y.rename(columns={'당기 1분기말':'매출채권_당기1분기말(연결)'}, inplace=True)
        jaemu1_y = jaemu1_y.drop_duplicates(['종목코드'], keep='last')
        
        # 1년전 재무상태표에서 매출채권 가져오기
        # 1. 별도
        jaemu1_ago = jaemu_data_ago[jaemu_data_ago['항목코드'].isin(['dart_ShortTermTradeReceivable', 'ifrs-full_TradeAndOtherCurrentReceivables'])]
        jaemu1_ago.rename(columns={'당기 1분기말':'매출채권_전기1분기말'}, inplace=True)
        jaemu1_ago = jaemu1_ago.drop_duplicates(['종목코드'], keep='last') # 중목 중 마지막 행 제거
        # 2. 연결
        jaemu1_ago_y = jaemu_data_ago[jaemu_data_ago['항목코드'].isin(['dart_ShortTermTradeReceivable', 'ifrs-full_TradeAndOtherCurrentReceivables'])]
        jaemu1_ago_y.rename(columns={'당기 1분기말':'매출채권_전기1분기말(연결)'}, inplace=True)
        jaemu1_ago_y = jaemu1_ago_y.drop_duplicates(['종목코드'], keep='last')
        
        
        #### 매출채권회전율, 매출채권회수기간 구하기 ####
        # 매출채권 = (기초 매출채권 + 기말매출채권) / 2
        # 매출채권회전율 = 매출액 / 매출채권
        # 매출채권회수기간 = 365 / 매출채권회전율
        
        ## 1. 포괄손익계산서_별도 + 재무상태표_별도 ##
        # ,빼고 float으로 만들기
        jaemu1_ago = jaemu1_ago.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik1 = posonik1.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        t_recv = pd.merge(jaemu1,jaemu1_ago,how='outer',on=['종목코드'])
        t_recv = pd.merge(t_recv,posonik1,how='outer',on=['종목코드'])
        t_recv.iloc[:,1:] = t_recv.iloc[:,1:].replace(',','',regex=True)
        
        # 전체를 numeric으로 변환하기
        a = 6
        row_count = len(t_recv.columns)
        exit = True
        
        while exit:
            t_recv.iloc[:,a] = pd.to_numeric(t_recv.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                exit = False
        
        # 매출채권 = (기초 매출채권 + 기말매출채권) / 2 구하기
        t_recv['real_recv'] = (t_recv['매출채권_당기1분기말'] + t_recv['매출채권_전기1분기말']) / 2
        
        # 매출채권회전율 구하기 : 매출채권회전율 = 매출액 / 매출채권
        t_recv['turnover'] = t_recv['(포)매출액_당기1분기3개월'] / t_recv['real_recv']
        
        # 매출채권회수기간 구하기
        t_recv['term'] = 365 / t_recv['turnover']
        
        # 회전율(turnover) 3이하, 회수기간(term) 150일 이상은 부적정
        recv_name = []
        for i in t_recv.index:
            if t_recv.loc[i,'term'] >= 150:
                recv_name.append(t_recv.loc[i,'회사명'])
        
        #print('별도:',recv_name)
        #print('별도개수:',len(recv_name))
        
        ## 2. 포괄손익계산서_연결 + 재무상태표_연결 ##
        jaemu1_ago_y = jaemu1_ago_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik1_y = posonik1_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        t_recv_y = pd.merge(jaemu1_y,jaemu1_ago_y,how='outer',on=['종목코드'])
        t_recv_y = pd.merge(t_recv_y,posonik1_y,how='outer',on=['종목코드'])
        t_recv_y.iloc[:,1:] = t_recv_y.iloc[:,1:].replace(',','',regex=True)
        
        # 전체를 numeric으로 변환하기
        a = 6
        row_count = len(t_recv_y.columns)
        exit = True
        
        while exit:
            t_recv_y.iloc[:,a] = pd.to_numeric(t_recv_y.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                exit = False
        
        # 매출채권 = (기초 매출채권 + 기말매출채권) / 2 구하기
        t_recv_y['real_recv'] = (t_recv_y['매출채권_당기1분기말(연결)'] + t_recv_y['매출채권_전기1분기말(연결)']) / 2
        
        # 매출채권회전율 구하기 : 매출채권회전율 = 매출액 / 매출채권
        t_recv_y['turnover'] = t_recv_y['(포)매출액_당기1분기3개월(연결)'] / t_recv_y['real_recv']
        
        # 매출채권회수기간 구하기
        t_recv_y['term'] = 365 / t_recv_y['turnover']
        
        # 회전율(turnover) 3이하, 회수기간(term) 150일 이상은 부적정
        recv_name_y = []
        for i in t_recv_y.index:
            if t_recv_y.loc[i,'term'] >= 150:
                recv_name_y.append(t_recv.loc[i,'회사명'])
        
        #print('연결:',recv_name_y)
        #print('연결개수:',len(recv_name_y))

        
        ####################################################################
        #리턴값을 입력하시오#
        return recv_name_y
        
        ####################################################################