import sys
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ebest.ebestlogin import *
from Kiwoom.kiwoomlogin import Login_Kiwoom
from etc.report1 import report1
from etc.report2 import report2
from etc.report3 import report3
from etc.report4 import report4
import pandas as pd


form_class = uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ### 다른 모듈의 객체 생성 모음 ###
        # report1.py를 연결하고 그 객체를 conn2으로 저장
        self.conn2 = report1()
        # report2.py를 연결하고 그 객체를 conn2_2으로 저장
        self.conn2_2 = report2()
        # report3.py를 연결하고 그 객체를 conn2_3으로 저장
        self.conn2_3 = report3()
        # report4.py를 연결하고 그 객체를 conn2_4으로 저장
        self.conn2_4 = report4()
        # 키움증권 로그인
        self.conn3 = Login_Kiwoom()
        # ebestlogin.py를 연결하고 그 객체를 conn5으로 저장
        self.conn5 = Login_Ebest()
        # 이베스트의 로그인 상태 확인 클래스(XASessionEvents)의 객체 생성
        self.conn5_1 = XASessionEvents()
        
        
        ### checkBox를 활성화 ###
        # self.checkBox.setChecked(True)


        ### 버튼 클릭 시 이벤트 모음 ###
        # 종목명 입력 후 엔터를 누를 시 종목 찾기
        self.gb3line1.returnPressed.connect(self.btn_clicked3)
        # 종목명 입력 후 찾기 버튼 누를 시 종목 찾기
        self.gb3button1.clicked.connect(self.btn_clicked3)
        # 장기투자종목 조회하기
        self.gb2button1.clicked.connect(self.Jongmog_Search)
        # 키움로그인 버튼 클릭
        self.Login_Kiwoom.clicked.connect(self.Login_Kiwoom_clicked)
        # 이베스트로그인 버튼 클릭
        self.Login_Ebest.clicked.connect(self.Login_Ebest_clicked)
        # 연결상태확인 버튼 클릭 시
        self.Conn_State.clicked.connect(self.Conn_State_clicked)

        
        # 테이블위젯1 = setEditTriggers 메서드를 사용해 사용자가 QTableWidget의 아이템 항목을 수정할 수 없도록 설정
        self.tableWidget_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 테이블위젯2 = setEditTriggers 메서드를 사용해 사용자가 QTableWidget의 아이템 항목을 수정할 수 없도록 설정
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # setTableWidgetData라는 함수 부르기(초기화)
        self.setTableWidgetData()

    # tableWidget_2에 해더에 라벨을 종목명 코드명으로 지정
    def setTableWidgetData(self):
        # row 방향에 대한 라벨을 설정할 때는 setVerticalHeaderLabels 메서드를 사용
        nameList = ["종목명","코드명"]
        self.tableWidget_2.setHorizontalHeaderLabels(nameList)

    # 전체 종목 조회하기 버튼
    def btn_clicked3(self):
        column_idx_lookup = {'name' : 0 , 'code' : 1}

        name = self.gb3line1.text()
        
        # 종목명의 체크박스에 체크가 된다면
        if self.checkBox.isChecked():
            self.conn.SearchNameListByName(name)
            rowCnt = len(self.conn.dataDict['name'])
            self.tableWidget_2.setRowCount(rowCnt)
            for k,v in self.conn.dataDict.items() :
                #print('k는 :',k) # k는 name과 code
                #print('v는:',v) # v는 종목명 리스트, 종목코드 리스트
                col = column_idx_lookup[k]
                #print('col는:',col)
                # enumerate 함수 = 리스트가 있는 경우 순서와 리스트의 값을 전달하는 기능을 가짐
                for row,val in enumerate(v) :
                    #print('row는?',row) # 0,1,2,3 ... = 인덱스
                    #print('val는?',val) # 인덱스의 값을 나타냄
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(val)))
        
        # 종목코드의 체크박스에 체크가 된다면
        elif self.checkBox_2.isChecked() :
            self.conn.SearchNameListByCode(name)
            rowCnt = len(self.conn.dataDict['name'])
            self.tableWidget_2.setRowCount(rowCnt)
            for k, v in self.conn.dataDict.items():
                col = column_idx_lookup[k]
                for row, val in enumerate(v):
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(val)))

    ### 버튼클릭시 이벤트 모음 ###
    # 키움로그인 버튼 클릭시 이벤트 
    def Login_Kiwoom_clicked(self):
        self.conn3.login()
        #self.kiwoom.dynamicCall("CommConnect()")
    
    # 이베스트로그인 버튼 클릭시 이벤트
    def Login_Ebest_clicked(self):
        self.conn5.Login()
    
    # 연결상태확인 버튼 클릭 시 이벤트
    def Conn_State_clicked(self):
        # 이베스트증권 연결 상태를 Line_conn3 라인에디트에 표시
        if self.conn5_1.logInState == 1:
            self.Line_conn3.setText("Connect")
        else:
            self.Line_conn3.setText("Disconnect")

    def Jongmog_Search(self):
        # 가져올 년도를 변수로 만들기, 보고서를 데이터 프레임으로 가져오기
        year = '2016'
        #df = self.conn2.report1(year)
        #df = self.conn2_2.report2(year)
        #df = self.conn2_3.report3(year)
        df = self.conn2_4.report4(year)
        
        # 데이터 프레임의 컬럼을 리스트화하기
        col = df.columns
        col = col.to_list()
        print(col)
        
        # setHorizontalHeaderLabels 메소드를 이용해서 컬럼값을 표시
        self.tableWidget_1.setHorizontalHeaderLabels(col)
        
        self.tableWidget_1.setColumnCount(len(df.columns))
        self.tableWidget_1.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.tableWidget_1.setItem(i,j,QTableWidgetItem(str(df.iloc[i, j])))

           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
    