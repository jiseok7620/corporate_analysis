# 투자 하지말아야 할 위기종목들 제외하기

import pandas as pd
import datetime
from screen1.hyengum_flow import hyen_flow
from screen1.trade_receivable import trade_receivable
from screen1.publish_jusik import publish_jusik
from screen1.debt_ratio import debt_ratio


# 현재 날짜 및 시간 나타내기
now = datetime.datetime.now()
#print(now)

# 년, 월, 일만 나타내기
# D:\oneday_csv\alldata의 파일을 그날에 따라 자동으로 읽기위함
nowDate = now.strftime('%Y%m%d')
#print(nowDate)

# 요일 나타내기
# 월 = 0 ~ 일 = 6
weekDay = datetime.datetime.today().weekday()
#print(weekDay)

# 토요일일 경우 -1, 일요일일 경우 -2를 실시하는 로직
# 토요일, 일요일인 경우에는 주식이 개장하지 않으므로

if weekDay == 5:
    nowDate = int(nowDate)
    nowDate = nowDate - 1
    nowDate = str(nowDate)
    print('불러올 하루 csv : ', nowDate)
elif weekDay == 6:
    nowDate = int(nowDate)
    nowDate = nowDate - 2
    nowDate = str(nowDate)
    print('불러올 하루 csv : ', nowDate)
else:
    print('불러올 하루 csv : ', nowDate)

# 해당 일자에 맞는 하루 전체 데이터 가져오기
try:
    today_csv = pd.read_csv("D:/oneday_csv/alldata/"+nowDate +".csv", encoding='cp949')
    print(today_csv)
except FileNotFoundError as e:
    print('금일 파일이 없습니다. 파일은 다운로드 받으세요.')


##########################################################################################
##########################################################################################
#### 화면1의 모듈들의 객체를 형성하기 ####
conn1 = hyen_flow() # 영업, 투자, 재무 현금흐름을 분석해서 투자에 부적정한 기업을 걸러내기
conn2 = trade_receivable() # 매출채권회전율 = 매출액 / 매출채권로 부적정한 기업 걸러내기
conn3 = publish_jusik() # 발행한 주식수가 몇년사이 엄청많아졌다?? => 증자를 많이 했다 => 안좋은 회사다
conn4 = debt_ratio() # 부채비율이 200% 이상인 기업 제외하기
 

print("현금흐름표 추출 종목 수 :", len(conn1.result_flow()))
print("매출채권 추출 종목 수 : ", len(conn2.result_receivable()))
print("발행주식 추출 종목 수 : ", conn3.publish_jusik())
print("부채비율 추출 종목 수 : ", len(conn4.result_debt("yes")))
###################################

'''
##### 배열 만들기 #####
hyen_flow_array = conn1.result_flow()
trade_receivable_array = conn2.result_receivable()
#####################################################

###### 배열 합치기 #####
all_data = hyen_flow_array + trade_receivable_array
#print(all_data)
#print(len(all_data))
#######################################################

###### 배열 중복 제거하기 ######
all_data = set(all_data)
all_data = list(all_data)
#print(all_data)
#print(len(all_data))
#######################################################
'''