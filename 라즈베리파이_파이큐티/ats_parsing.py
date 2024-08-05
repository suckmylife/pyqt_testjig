from PyQt5.QtCore import pyqtSignal,QObject,QTimer
from datetime import datetime
import numpy as np
#버튼 시그널(녹화버튼, 카운트 버튼) 알 수 있는 모듈 추가 
import ats_database
import ats_visualize


#통신프로토콜 
HEADER = '7ee7'
SEND = '4D'
RESPONSE = '53'
COMMAND = '81'
START_PRESSURE = 12
END_PRESSURE = 44
#저장 시간 
TIME = 1000

#데이터
parsing = []

#파싱해서 데이터베이스에 넘기기 필요한것. 넘버링, 주소, 공압값
#파싱해서 히트맵에 넘기기 공압값만 

def calculate_checksum(data):
    checksum1 = 0
    # QByteArray를 바이트열로 변환
    byte_data = bytes(data)
    # 2개씩 끊어진 바이트 묶음을 처리하고 총합 계산
    checksum1 = sum(int(byte_data[i:i+2].decode(), 16) for i in range(0, len(byte_data)-2, 2))

    twos = 0xFF - (checksum1 & 0xFF)
    twos_hex = format(twos, '02X')  # 2자리 16진수로 변환
    return twos_hex


class Parsing(QObject):
    global START_PRESSURE
    global END_PRESSURE
    data_signal = pyqtSignal(dict)

    def __init__(self,parent=None):
        super().__init__(parent)

        self.address = 0
        self.numbering = 0

        self.timer = QTimer()

        self.db = ats_database.connectdb()
        self.vis = ats_visualize.visual_widget()

        self.env_id = ats_database.ENV_ID

    
    def start_timer(self):
        self.timer.timeout.connect(self.save_rec)
        self.timer.start(TIME)
    
    def stop_timer(self):
        self.timer.stop()
    
    def plus_counting(self,value):
        ats_visualize.set_counting(value)

    #녹화버튼
    def DB_rec(self,response):
        length = len(response)
        blank = []
        global parsing
        self.env_id = ats_database.ENV_ID

        for i in range(0,length):
            res = str(response[i],'utf-8')
            checksum = calculate_checksum(response[i])
            if (HEADER == res[0:4] and len(res)>43 and res[-2:].upper() == checksum):
                self.address = res[8:10]
                self.numbering = 0
                pressure = res[START_PRESSURE:END_PRESSURE]
                result = [float(int(pressure[i:i+4],16)/10) for i in range(0, len(pressure), 4)]
                blank.append({
                    'air_date' : datetime.now().strftime('%Y-%m-%d'),
                    'air_time' : datetime.now().time().strftime('%H:%M:%S'),
                    'air_pressure' : ','.join(map(str, result)),
                    'cnt' : self.numbering, 
                    'channel' : self.address, 
                    'env_id' : self.env_id
                    })
        parsing = blank[0]
    
    def save_rec(self):
        global parsing
        if len(parsing)>0:
            self.db.save_rec(parsing)
            parsing = []
    
    #실시간 모니터링
    def parse_realtime(self,response):
        length = len(response)
        data_dict = {}
        for i in range(0,length):
            res = str(response[i],'utf-8')
            checksum = calculate_checksum(response[i])
            if (HEADER == res[0:4] and len(res)>43 and res[-2:].upper() == checksum):
                self.address = res[8:10] #히트맵 그릴 위치 
                pressure = res[START_PRESSURE:END_PRESSURE] #히트맵에 넘길 데이터 
                result = [float(int(pressure[i:i+4],16)/10) for i in range(0, len(pressure), 4)]
                data_dict[int(self.address,16)] = np.array(result).reshape((2,4))
        if bool(data_dict):
            # 주어진 dict 데이터를 4x2 형태로 변환하여 data_dict에 저장
            self.vis.setting_data(data_dict)
        

    #카운트 버튼 
    def DB_cnt(self,response):
        length = len(response)
        self.env_id = ats_database.ENV_ID
        
        for i in range(0,length):
            res = str(response[i],'utf-8')
            checksum = calculate_checksum(response[i])
            datas = []
            if (HEADER == res[0:4] and len(res)>43 and res[-2:].upper() == checksum):
                self.address = res[8:10]
                self.plus_counting(1)
                pressure = res[START_PRESSURE:END_PRESSURE]
                result = [float(int(pressure[i:i+4],16)/10) for i in range(0, len(pressure), 4)]
                datas.append({
                    'cnt_air_date' : datetime.now().strftime('%Y-%m-%d'),  
                    'cnt_air_time' : datetime.now().time().strftime('%H:%M:%S'),
                    'cnt_air_pressure' : ','.join(map(str, result)),
                    'cnt' : ats_visualize.get_counting(),
                    'cnt_channel' :self.address,
                    'env_id' :self.env_id
                    })
                self.db.save_cnt(datas[0])
