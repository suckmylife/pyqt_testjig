from PyQt5.QtWidgets import QWidget, QMessageBox,QTableWidgetItem
from PyQt5.QtGui import QIcon
from openpyxl import Workbook
import pymysql
import requests
# 데이터베이스 연결 정보
DB_HOST = '172.47.20.224'
DB_PORT = 3305
DB_NAME = 'AirMatTestSystem'
DB_USER = 'neoable'
DB_PASS = '^Neoable1234'
import neo
#환경 번호 
ENV_ID = 0
#페이지 번호
pg_prev_num = None
pg_nxt_num = None
#버전 관리
board_ver = None
aircell_ver = None
sw_ver = 0
#로그인 세션 관리
user_ID = None
class connectdb(QWidget):
    def __init__(self):
        super().__init__()
        #아이콘 설정
        self.icon = QIcon(":/neo/neoable.png")
        # MySQL 서버 연결 정보 설정
        self.conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASS,
            db=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def messagebox(self,types,title,text):
        msg = QMessageBox()
        if types == "info":
            msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setWindowIcon(self.icon)
        msg.exec_()

    #로그인 검증 함수
    def login_verify(self,id,psw):
        global user_ID
        data = {
            'id': id,
            'password': psw
        }
        try:
            response = requests.post('http://183.101.208.34:80/login', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    if result['result'] == 'valid':
                        user_ID = id
                        return True
                    else:
                        types = 'info'
                        title = '실패'
                        text = '아이디와 비밀번호를 확인해주세요'
                        self.messagebox(types,title,text)
                        return False
            else:
                types = 'info'
                title = '실패'
                text = '웹서버를 확인해 주세요'
                self.messagebox(types,title,text)
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
        
    #실험환경 저장 함수 
    def save_env(self,env_name,exp_name,exp_info,p_name,p_tall,p_age,p_gender,p_weight):
        global ENV_ID
        global board_ver
        global aircell_ver
        global user_ID

        data = {
            'env_name' : env_name,
            'exp_name' : exp_name,
            'exp_info' : exp_info,
            'p_name' : p_name,
            'p_tall' : p_tall,
            'p_age' : p_age,
            'p_gender' : p_gender,
            'p_weight' : p_weight,
            'board_ver': board_ver,
            'aircell_ver' : aircell_ver,
            'userID' : user_ID
        }

        try:
            response = requests.post('http://183.101.208.34:80/save_env', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    ENV_ID = result['lastrowid']
                else:
                    types = 'info'
                    title = '실패'
                    text = '저장 실패'
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to save_env")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #녹화버튼 클릭 후에 공압데이터 저장 함수 
    def save_rec(self,data):
        try:
            response = requests.post('http://183.101.208.34:80/save_rec', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    if result['result'] == "Success":
                        pass
                    else:
                        types = 'info'
                        title = '실패'
                        text = '저장 실패'
                        self.messagebox(types,title,text)
                        return False
            else:
                print("Failed to save_rec")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #카운트 버튼 클릭 후에 공압데이터 저장 함수 
    def save_cnt(self,data):
        try:
            response = requests.post('http://183.101.208.34:80/save_cnt', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    if result['result'] == "Success":
                        pass
                    else:
                        types = 'info'
                        title = '실패'
                        text = '저장 실패'
                        self.messagebox(types,title,text)
                        return False
            else:
                print("Failed to save_cnt")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #조회된 카운트 데이터 테이블 위젯에 넣는 함수 
    def create_table(self,table,rows,state="normal"):
        global pg_nxt_num
        global pg_prev_num
        table.setRowCount(len(rows))
        table.setColumnCount(len(rows[0]))
        if state == "normal":
            for row, item in enumerate(rows):
                env_id_item = QTableWidgetItem(str(item['env_id']))  # env_id 값을 문자열로 변환하여 QTableWidgetItem 생성
                exp_name_item = QTableWidgetItem(item['exp_name'])  # exp_name 값을 QTableWidgetItem 생성
                cnt_air_date_item = QTableWidgetItem(item['cnt_air_date'])  # cnt_air_date 값을 QTableWidgetItem 생성

                table.setItem(row, 0, env_id_item)  # 테이블의 특정 위치(row, column)에 QTableWidgetItem 설정
                table.setItem(row, 1, exp_name_item)
                table.setItem(row, 2, cnt_air_date_item)

            table.resizeColumnsToContents()  # 열의 크기를 콘텐츠에 맞게 조정
        else:
            for row, item in enumerate(reversed(rows)):
                env_id_item = QTableWidgetItem(str(item['env_id']))  # env_id 값을 문자열로 변환하여 QTableWidgetItem 생성
                exp_name_item = QTableWidgetItem(item['exp_name'])  # exp_name 값을 QTableWidgetItem 생성
                cnt_air_date_item = QTableWidgetItem(item['cnt_air_date'])  # cnt_air_date 값을 QTableWidgetItem 생성

                table.setItem(row, 0, env_id_item)  # 테이블의 특정 위치(row, column)에 QTableWidgetItem 설정
                table.setItem(row, 1, exp_name_item)
                table.setItem(row, 2, cnt_air_date_item)
            table.resizeColumnsToContents()  # 열의 크기를 콘텐츠에 맞게 조정
        # 컬럼 헤더 설정
        headers = ["no.","env-name","date"]
        table.setHorizontalHeaderLabels(headers)
        last_row_index = table.rowCount() - 1
        pg_nxt_num = int(table.item(last_row_index,0).text())
        pg_prev_num = int(table.item(0,0).text())

    #카운트 데이터 조회 함수 
    def call_cnt(self, table, state, date=[]):
        global pg_nxt_num
        global pg_prev_num
        data ={
            'pg_prev_num' : pg_prev_num,
            'pg_nxt_num' : pg_nxt_num,
            'state' : state,
            'date' : date
        }
        try:
            response = requests.post('http://183.101.208.34:80/call_cnt', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    rows = result['result']
                    if rows:
                        self.create_table(table, rows)
                    else:
                        if state == 'init':
                            self.messagebox('info','안내','데이터가 없습니다')
                        elif state == 'next':
                            self.messagebox('info','안내','마지막 페이지입니다')
                        elif state == 'prev':
                            self.messagebox('info','안내','첫 번째 페이지입니다')
                else:
                    types = 'info'
                    title = '실패'
                    text = result
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to call_cnt")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #카운트 데이터에 따른 세부 내용 조회 함수 
    def call_cnt_info(self,label,search_no):
        global board_ver
        global aircell_ver
        data = {
            'env_id' : search_no
        }
        rows = []
        try:
            response = requests.post('http://183.101.208.34:80/call_cnt_info', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    rows = result['result']
                    label.exl_user_name.setText(str(rows[0]['exp_name']))
                    label.exl_patient_name.setText(str(rows[0]['patient_name']))
                    label.exl_patient_age.setText(str(rows[0]['patient_age']))
                    label.exl_patient_gender.setText(str(rows[0]['patient_gender']))
                    label.exl_patient_tall.setText(str(rows[0]['patient_tall']))
                    label.exl_patient_weight.setText(str(rows[0]['patient_weight']))
                    label.exl_patient_info.setText(str(rows[0]['exp_info']))
                    label.cte_board_ver.setText(board_ver)
                    label.cte_aircell_ver.setText(aircell_ver)
                else:
                    types = 'info'
                    title = '실패'
                    text = result
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to call_cnt_info")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
    
    #테이블 위젯에 있는 카운트 데이터 실험명 편집 함수
    def edit_update(self,new_name,id):
        data = {
            'env_id' : id,
            'new_env_name' : new_name
        }
        try:
            response = requests.post('http://183.101.208.34:80/edit_update', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    if result['result'] == "Success":
                        pass
                    else:
                        types = 'info'
                        title = '실패'
                        text = result
                        self.messagebox(types,title,text)
                        return False
            else:
                print("Failed to edit_update")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #테이블 위젯 옆에 세부항목에 대한 편집 함수 
    def detail_edit_update(self,condition,data,id):
        data = {
            'condition' : condition,
            'info' : data,
            'id' : id
        }
        try:
            response = requests.post('http://183.101.208.34:80/detail_edit_update', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    if result['result'] == "Success":
                        pass
                    else:
                        types = 'info'
                        title = '실패'
                        text = '저장 실패'
                        self.messagebox(types,title,text)
                        return False
            else:
                print("Failed to detail_edit_update")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #카운트 데이터 엑셀로 변환하는 함수 
    def convert_exl(self,date,id):
        data = {
            'date':date,
            'id': id
        }
        pressure = []
        try:
            response = requests.post('http://183.101.208.34:80/convert_exl', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,list):
                    pressure = result
                    excel = Workbook()
                    exl_sheet = excel.active

                    header = ["시간","위치","카운트",1,2,3,4,5,6,7,8]      
                    exl_sheet.append(header)
                    for row_data in pressure:
                        cnt_air_pressure = [float(x) for x in row_data['cnt_air_pressure'].split(',')]
                        cnt = row_data['cnt']
                        cnt_channel = row_data['cnt_channel']
                        cnt_air_time = row_data['cnt_air_time']

                        dicts = [cnt_air_time, cnt_channel, cnt] + cnt_air_pressure
                        exl_sheet.append(dicts)

                    save_file_name = f"{date}_{id}_네오에이블_공압센서_실험파일.xlsx"
                    excel.save(save_file_name)  
                    types = 'info'
                    title = '완료'
                    text = '엑셀파일이 저장되었습니다'
                    self.messagebox(types,title,text)
                else:
                    types = 'info'
                    title = '실패'
                    text = result
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to convert_exl")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
    
    #보드 버전 조회 함수 
    def call_board(self,ui,condition=None):
        global board_ver
        data = {
            'condition':condition
        }
        try:
            response = requests.post('http://183.101.208.34:80/call_board', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    rows = result['result']
                    ui.vs_board_ver.setText(str(rows[0]['board_ver']))
                    ui.vs_board_info.setText(str(rows[0]['board_info']))
                    ui.vs_board_update.setText(str(rows[0]['board_update_date']))
                    if condition is None:
                        board_ver = str(rows[0]['board_ver'])

                        for item in rows:
                            ui.board_combo.addItem(item['board_ver'])
                else:
                    types = 'info'
                    title = '실패'
                    text = '저장 실패'
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to call_board")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

            

    #에어셀 버전 조회 함수 
    def call_aircell(self,ui,condition=None):
        global aircell_ver
        data = {
            'condition':condition
        }
        try:
            response = requests.post('http://183.101.208.34:80/call_aircell', json=data)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    rows = result['result']
                    ui.vs_aircell_ver.setText(str(rows[0]['aircell_ver']))
                    ui.vs_aircell_info.setText(str(rows[0]['aircell_info']))
                    ui.vs_aircell_update.setText(str(rows[0]['aircell_update_date']))
                    if condition is None:
                        aircell_ver = str(rows[0]['aircell_ver'])

                        for item in rows:
                            ui.aircell_combo.addItem(item['aircell_ver'])
                else:
                    types = 'info'
                    title = '실패'
                    text = '조회 실패'
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed call_aircell")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

    #소프트웨어 버전 조회 함수 
    def call_sw(self,ui):
        try:
            response = requests.post('http://183.101.208.34:80/call_sw')
            if response.status_code == 200:
                result = response.json()
                if isinstance(result,dict):
                    rows = result['result']
                    ui.vs_sw_ver.setText(str(rows['sw_ver']))
                    ui.vs_sw_info.setText(str(rows['sw_info']))
                    ui.vs_sw_update.setText(str(rows['sw_update_date']))
                else:
                    types = 'info'
                    title = '실패'
                    text = '저장 실패'
                    self.messagebox(types,title,text)
                    return False
            else:
                print("Failed to call_sw")
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))

        