# 반기보고서 가져오기

import pandas as pd
import openpyxl # pip install xlwt, pip install openpyxl

class report2:
    def report2(self, year):
        # csv를 데이터프레임으로 저장하기
        self.df_hyen = pd.read_csv('D:/report_csv/report/'+year+'_2_hyen.csv', encoding='cp949')
        self.df_hyen_y = pd.read_csv('D:/report_csv/report/'+year+'_2_hyen_y.csv', encoding='cp949')
        self.df_jaemu = pd.read_csv('D:/report_csv/report/'+year+'_2_jaemu.csv', encoding='cp949')
        self.df_jaemu_y = pd.read_csv('D:/report_csv/report/'+year+'_2_jaemu_y.csv', encoding='cp949')
        self.df_posonik = pd.read_csv('D:/report_csv/report/'+year+'_2_posonik.csv', encoding='cp949')
        self.df_posonik_y = pd.read_csv('D:/report_csv/report/'+year+'_2_posonik_y.csv', encoding='cp949')
        
        # 데이터 정제하기(필요없는 열 제거하기)
        self.df_hyen = self.df_hyen.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기 반기', '전기', '전전기'], axis=1)
        self.df_hyen_y = self.df_hyen_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기 반기', '전기','전전기'], axis=1)
        self.df_jaemu = self.df_jaemu.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기말', '전전기말'], axis=1)
        self.df_jaemu_y = self.df_jaemu_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '전기말', '전전기말'], axis=1)
        self.df_posonik = self.df_posonik.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '당기 반기 누적', '전기 반기 3개월', '전기 반기 누적', '전기', '전전기'], axis=1)
        self.df_posonik_y= self.df_posonik_y.drop(['재무제표종류','시장구분','결산월','결산기준일','보고서종류','통화', '당기 반기 누적', '전기 반기 3개월', '전기 반기 누적', '전기', '전전기'], axis=1)
        
        # 데이터 정제하기(각 데이터 프레임에서 필요한 항목만 가져오기)
        ## 1. 현금흐름표 : 영업활동 현금흐름(ifrs-full_CashFlowsFromUsedInOperatingActivities), 
        #투자활동 현금흐름(ifrs-full_CashFlowsFromUsedInInvestingActivities), 재무활동 현금흐름(ifrs-full_CashFlowsFromUsedInFinancingActivities)
        hyen1 = self.df_hyen[self.df_hyen['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1.rename(columns={'당기 반기':'영업현금흐름_당기반기'}, inplace=True)
        
        hyen2 = self.df_hyen[self.df_hyen['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2 = hyen2.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen2.rename(columns={'당기 반기':'투자현금흐름_당기반기'}, inplace=True)
        
        hyen3 = self.df_hyen[self.df_hyen['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3 = hyen3.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen3.rename(columns={'당기 반기':'재무현금흐름_당기반기'}, inplace=True)
        
        hyen = pd.merge(hyen1,hyen2, how='outer', on=['종목코드'])
        hyen = pd.merge(hyen,hyen3, how='outer', on=['종목코드'])
        hyen = hyen.drop_duplicates(['종목코드'])
        #print(hyen)
        
        ## 2. 현금흐름표_연결 : 영업활동 현금흐름(ifrs-full_CashFlowsFromUsedInOperatingActivities), 
        #투자활동 현금흐름(ifrs-full_CashFlowsFromUsedInInvestingActivities), 재무활동 현금흐름(ifrs-full_CashFlowsFromUsedInFinancingActivities)
        hyen1_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1_y.rename(columns={'당기 반기':'영업현금흐름_당기반기_연결'}, inplace=True)
        
        hyen2_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2_y = hyen2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen2_y.rename(columns={'당기 반기':'투자현금흐름_당기반기_연결'}, inplace=True)
        
        hyen3_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3_y = hyen3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen3_y.rename(columns={'당기 반기':'재무현금흐름_당기반기_연결'}, inplace=True)
        
        hyen_y = pd.merge(hyen1_y,hyen2_y, how='outer', on=['종목코드'])
        hyen_y = pd.merge(hyen_y,hyen3_y, how='outer', on=['종목코드'])
        hyen_y = hyen_y.drop_duplicates(['종목코드'])
        #print(hyen_y)
        
        ## 3. 재무상태표 : 유동자산(ifrs-full_CurrentAssets), 비유동자산(ifrs-full_NoncurrentAssets), 자산총계(ifrs-full_Assets)
        # 유동부채(ifrs-full_CurrentLiabilities), 비유동부채(ifrs-full_NoncurrentLiabilities), 부채총계(ifrs-full_Liabilities)
        # 자본금(ifrs-full_IssuedCapital), 이익잉여금(ifrs-full_RetainedEarnings), 자본총계(ifrs-full_Equity)
        jaemu1 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_CurrentAssets'])]
        jaemu1.rename(columns={'당기 반기말':'유동자산_당기반기말'}, inplace=True)
        
        jaemu2 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_NoncurrentAssets'])]
        jaemu2 = jaemu2.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu2.rename(columns={'당기 반기말':'비유동자산_당기반기말'}, inplace=True)
        
        jaemu3 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_Assets'])]
        jaemu3 = jaemu3.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu3.rename(columns={'당기 반기말':'자산총계_당기반기말'}, inplace=True)
        
        jaemu4 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_CurrentLiabilities'])]
        jaemu4 = jaemu4.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu4.rename(columns={'당기 반기말':'유동부채_당기반기말'}, inplace=True)
        
        jaemu5 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_NoncurrentLiabilities'])]
        jaemu5 = jaemu5.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu5.rename(columns={'당기 반기말':'비유동부채_당기반기말'}, inplace=True)
        
        jaemu6 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_Liabilities'])]
        jaemu6 = jaemu6.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu6.rename(columns={'당기 반기말':'부채총계_당기반기말'}, inplace=True)
        
        jaemu7 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_IssuedCapital'])]
        jaemu7 = jaemu7.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu7.rename(columns={'당기 반기말':'자본금_당기반기말'}, inplace=True)
        
        jaemu8 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_RetainedEarnings'])]
        jaemu8 = jaemu8.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu8.rename(columns={'당기 반기말':'이익잉여금_당기반기말'}, inplace=True)
        
        jaemu9 = self.df_jaemu[self.df_jaemu['항목코드'].isin(['ifrs-full_Equity'])]
        jaemu9 = jaemu9.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu9.rename(columns={'당기 반기말':'자본총계_당기반기말'}, inplace=True)
        
        jaemu = pd.merge(jaemu1,jaemu2,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu3,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu4,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu5,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu6,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu7,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu8,how='outer',on=['종목코드'])
        jaemu = pd.merge(jaemu,jaemu9,how='outer',on=['종목코드'])
        jaemu = jaemu.drop_duplicates(['종목코드'])
        
        #print(jaemu)
        
        ## 4. 재무상태표_연결 : 유동자산(ifrs-full_CurrentAssets), 비유동자산(ifrs-full_NoncurrentAssets), 자산총계(ifrs-full_Assets)
        # 유동부채(ifrs-full_CurrentLiabilities), 비유동부채(ifrs-full_NoncurrentLiabilities), 부채총계(ifrs-full_Liabilities)
        # 자본금(ifrs-full_IssuedCapital), 이익잉여금(ifrs-full_RetainedEarnings), 자본총계(ifrs-full_Equity)
        jaemu1_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_CurrentAssets'])]
        jaemu1_y.rename(columns={'당기 반기말':'유동자산_당기반기말_연결'}, inplace=True)
        
        jaemu2_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_NoncurrentAssets'])]
        jaemu2_y = jaemu2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu2_y.rename(columns={'당기 반기말':'비유동자산_당기반기말_연결'}, inplace=True)
        
        jaemu3_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_Assets'])]
        jaemu3_y = jaemu3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu3_y.rename(columns={'당기 반기말':'자산총계_당기반기말_연결'}, inplace=True)
        
        jaemu4_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_CurrentLiabilities'])]
        jaemu4_y = jaemu4_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu4_y.rename(columns={'당기 반기말':'유동부채_당기반기말_연결'}, inplace=True)
        
        jaemu5_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_NoncurrentLiabilities'])]
        jaemu5_y = jaemu5_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu5_y.rename(columns={'당기 반기말':'비유동부채_당기반기말_연결'}, inplace=True)
        
        jaemu6_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_Liabilities'])]
        jaemu6_y = jaemu6_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu6_y.rename(columns={'당기 반기말':'부채총계_당기반기말_연결'}, inplace=True)
        
        jaemu7_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_IssuedCapital'])]
        jaemu7_y = jaemu7_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu7_y.rename(columns={'당기 반기말':'자본금_당기반기말_연결'}, inplace=True)
        
        jaemu8_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_RetainedEarnings'])]
        jaemu8_y = jaemu8_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu8_y.rename(columns={'당기 반기말':'이익잉여금_당기반기말_연결'}, inplace=True)
        
        jaemu9_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs-full_Equity'])]
        jaemu9_y = jaemu9_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu9_y.rename(columns={'당기 반기말':'자본총계_당기반기말_연결'}, inplace=True)
        
        jaemu_y = pd.merge(jaemu1_y,jaemu2_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu3_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu4_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu5_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu6_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu7_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu8_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu9_y,how='outer',on=['종목코드'])
        jaemu_y = jaemu_y.drop_duplicates(['종목코드'])
        
        #print(jaemu_y)
        
        ## 포괄손익계산서 
        # 매출액(ifrs-full_Revenue), 매출원가(ifrs-full_CostOfSales), 매출총이익(ifrs-full_GrossProfit)
        # 판관비(dart_TotalSellingGeneralAdministrativeExpenses), 영업이익(dart_OperatingIncomeLoss)
        # 법인세비용차감전순이익(ifrs-full_ProfitLossBeforeTax)
        # 당기순이익(ifrs-full_ProfitLoss), 총포괄손익(ifrs-full_ComprehensiveIncome)
        posonik1 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_Revenue'])]
        posonik1.rename(columns={'당기 반기 3개월':'(포)매출액_당기반기3개월'}, inplace=True)
        
        posonik2 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_CostOfSales'])]
        posonik2 = posonik2.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik2.rename(columns={'당기 반기 3개월':'(포)매출원가_당기반기3개월'}, inplace=True)
        
        posonik3 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_GrossProfit'])]
        posonik3 = posonik3.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik3.rename(columns={'당기 반기 3개월':'(포)매출총이익_당기반기3개월'}, inplace=True)
        
        posonik4 = self.df_posonik[self.df_posonik['항목코드'].isin(['dart_TotalSellingGeneralAdministrativeExpenses'])]
        posonik4 = posonik4.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik4.rename(columns={'당기 반기 3개월':'(포)판관비_당기반기3개월'}, inplace=True)
        
        posonik5 = self.df_posonik[self.df_posonik['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        posonik5 = posonik5.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik5.rename(columns={'당기 반기 3개월':'(포)영업이익_당기반기3개월'}, inplace=True)
        
        posonik6 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_ProfitLossBeforeTax'])]
        posonik6 = posonik6.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik6.rename(columns={'당기 반기 3개월':'(포)법인세비용차감전순이익_당기반기3개월'}, inplace=True)
        
        posonik7 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_ProfitLoss'])]
        posonik7 = posonik7.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik7.rename(columns={'당기 반기 3개월':'(포)당기순이익_당기반기3개월'}, inplace=True)
        
        posonik8 = self.df_posonik[self.df_posonik['항목코드'].isin(['ifrs-full_ComprehensiveIncome'])]
        posonik8 = posonik8.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik8.rename(columns={'당기 반기 3개월':'(포)총포괄손익_당기반기3개월'}, inplace=True)
        
        posonik = pd.merge(posonik1,posonik2,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik3,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik4,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik5,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik6,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik7,how='outer',on=['종목코드'])
        posonik = pd.merge(posonik,posonik8,how='outer',on=['종목코드'])
        posonik = posonik.drop_duplicates(['종목코드'])
        
        #print(posonik)
        
        ## 포괄손익계산서_연결
        # 매출액(ifrs-full_Revenue), 매출원가(ifrs-full_CostOfSales), 매출총이익(ifrs-full_GrossProfit)
        # 판관비(dart_TotalSellingGeneralAdministrativeExpenses), 영업이익(dart_OperatingIncomeLoss)
        # 법인세비용차감전순이익(ifrs-full_ProfitLossBeforeTax)
        # 당기순이익(ifrs-full_ProfitLoss), 총포괄손익(ifrs-full_ComprehensiveIncome)
        posonik1_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_Revenue'])]
        posonik1_y.rename(columns={'당기 반기 3개월':'(포)매출액_당기반기3개월_연결'}, inplace=True)
        
        posonik2_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_CostOfSales'])]
        posonik2_y = posonik2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik2_y.rename(columns={'당기 반기 3개월':'(포)매출원가_당기반기3개월_연결'}, inplace=True)
        
        posonik3_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_GrossProfit'])]
        posonik3_y = posonik3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik3_y.rename(columns={'당기 반기 3개월':'(포)매출총이익_당기반기3개월_연결'}, inplace=True)
        
        posonik4_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['dart_TotalSellingGeneralAdministrativeExpenses'])]
        posonik4_y = posonik4_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik4_y.rename(columns={'당기 반기 3개월':'(포)판관비_당기반기3개월_연결'}, inplace=True)
        
        posonik5_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        posonik5_y = posonik5_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik5_y.rename(columns={'당기 반기 3개월':'(포)영업이익_당기반기3개월_연결'}, inplace=True)
        
        posonik6_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_ProfitLossBeforeTax'])]
        posonik6_y = posonik6_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik6_y.rename(columns={'당기 반기 3개월':'(포)법인세비용차감전순이익_당기반기3개월_연결'}, inplace=True)
        
        posonik7_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_ProfitLoss'])]
        posonik7_y = posonik7_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik7_y.rename(columns={'당기 반기 3개월':'(포)당기순이익_당기반기3개월_연결'}, inplace=True)
        
        posonik8_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs-full_ComprehensiveIncome'])]
        posonik8_y = posonik8_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik8_y.rename(columns={'당기 반기 3개월':'(포)총포괄손익_당기반기3개월_연결'}, inplace=True)
        
        posonik_y = pd.merge(posonik1_y,posonik2_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik3_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik4_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik5_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik6_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik7_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik8_y,how='outer',on=['종목코드'])
        posonik_y = posonik_y.drop_duplicates(['종목코드'])
        
        #print(posonik_y)
        
        
        ######################################################
        ################## 전체데이터 합치기 ####################
        # hyen, hyen_y, jaemu, jaemu_y, posonik, posonik_y, sonik, sonik_y
        # 1. 데이터에서 필요없는 열 제거
        hyen = hyen.drop(['항목명','항목코드'], axis=1)
        hyen_y = hyen_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu = jaemu.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu_y = jaemu_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik = posonik.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik_y = posonik_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        # 2.데이터 합치기
        # merge : pd.merge(데이터프레임1, 데이터프레임2, how='방법', on=None)
        # on=None 이면 교집합 조인을 하게됨
        final_data = pd.merge(hyen,hyen_y,how='outer',on=['종목코드'])
        final_data = pd.merge(final_data,jaemu,how='outer',on=['종목코드'])
        final_data = pd.merge(final_data,jaemu_y,how='outer',on=['종목코드'])
        final_data = pd.merge(final_data,posonik,how='outer',on=['종목코드'])
        final_data = pd.merge(final_data,posonik_y,how='outer',on=['종목코드'])
        final_data = final_data.drop_duplicates(['종목코드'])
        
        #print(final_data.shape)
        #print(final_data)
        return final_data
        #final_data.to_excel('final_data.xlsx')
        ################## 전체데이터 합치기 ######################
        ######################################################