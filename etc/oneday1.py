# 1. 폴더 생성하기
# 2. csv 파일 생성하기
# 3. csv 파일에 하루 종목 전체 추가하기

import pandas as pd
import os
import numpy as np
import csv
import datetime

# 폴더를 만드는 함수 구문
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

## 현재날짜 year:년도, q:분기, y: yes or no
now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')
        
# 연도 변수 선언
year = nowDate[0:4]

# 일일 전체종목 csv 파일을 모아놓은 폴더에서 csv의 이름을 추출
csv_files_collect = []
for path, dirs, files in os.walk("D:/oneday_csv/alldata"):
    print('files:',files)
    csv_files_collect = files
    

## 메인 로직 ##
for csvfile in csv_files_collect :
    df = pd.read_csv("D:/oneday_csv/alldata/" + csvfile, encoding='cp949')
    df.insert(0, '일자', csvfile[0:8]) 
    
    # 종목명을 리스트로 만들기
    a = []
    a = np.array(df['종목명'].tolist())

    # 종목의 수 만큼 for문으로 폴더만들기
    col_name = ['일자','종목코드', '종목명', '시장구분', '소속부', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '시가총액', '상장주식수']

    for i in a:    
        # 해당 종목에서 for문 빠져나오기
        #if i == 'BNK금융지주':
            #break;

        # 종목명을 이름으로 폴더만들기
        directory = 'D:/oneday_csv/onedaydata/' + i
        createFolder(directory)

        # 종목명을 이름으로 csv만들기
        csv_path = 'D:/oneday_csv/onedaydata/' + i + '/' + i + '.csv'
        if not os.path.exists(csv_path):
            f = open(csv_path, 'w', newline='', encoding='cp949')
            wr = csv.writer(f)
            wr.writerow(col_name)
            f.close() 
    

    # 생성된 csv에 데이터 추가하기
    for i in a:
        #if i == 'BNK금융지주':
            #break;
        
        # 변수 선언 및 초기화 구문
        yes_no = 'yes'
        file_path = 'D:/oneday_csv/onedaydata/' + i + '/' + i + '.csv'
        file_name = df['종목명'] == i
        file_list = df[file_name]
        
        ###### 만약에 해당 날짜가 존재하면 넣지않음 #########    
        k = open(file_path, 'r', encoding='cp949')
        while True: 
            line = k.readline()
            line_list = line.split(',')
            if line_list[0] == csvfile[0:8]:
                #print('추가 X')
                yes_no = 'no'
                break
            if not line: 
                break 
                #print(line.rstrip())
        ###############################################

        if os.path.exists(file_path) and yes_no == 'yes':
            f = open(file_path, 'a', newline='', encoding='cp949')
            wr = csv.writer(f)
            wr.writerow(file_list.iloc[0])
            f.close()