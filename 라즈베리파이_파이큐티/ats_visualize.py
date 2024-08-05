from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtCore import QTimer,pyqtSlot
from PyQt5.QtMultimedia import QSound
import numpy as np
import pyqtgraph as pg
#기능 모듈
import visualize_button
import ats_database
from ats_excel_pop import excel_pop_widget
import neo
from qrc_vis import Ui_visualize
#버튼 통신
is_cnt = False #카운트 버튼
is_rec = False #녹화 버튼
is_reset = False #카운트 리셋 버튼
is_pressure_reset = False #압력 리셋버튼 
is_address = False
counting = 0 #카운트 넘버링 
#데이터
g_data_dict = []
selected_checkbox = None
#히트맵 색깔 범위 
H_MIN = 1
H_MAX = 32
#저장 시간 
TIME = 1000

def set_selected_checkbox(value):
    global selected_checkbox
    selected_checkbox = value

def get_selected_checkbox():
    global selected_checkbox
    return selected_checkbox

def set_address(value):
    global is_address
    is_address = value

def get_address():
    global is_address
    return is_address

def set_counting(value):
    global counting
    if value == 0:
        counting = value
    else:
        counting += value

def get_counting():
    global counting
    return counting

def set_reset(value):
    global is_reset
    is_reset = value

def get_reset():
    global is_reset
    return is_reset

def set_p_reset(value):
    global is_pressure_reset
    is_pressure_reset = value

def get_p_reset():
    global is_pressure_reset
    return is_pressure_reset

def set_cnt(value):
    global is_cnt
    is_cnt = value

def get_cnt():
    global is_cnt
    return is_cnt

def set_record(value):
    global is_rec
    is_rec = value

def get_record():
    global is_rec
    return is_rec

class visual_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_visualize()
        self.ui.setupUi(self)
        #환경 저장
        self.db = ats_database.connectdb()
        #해상도 자동크기 조절
        self.ui.title1.setWordWrap(True)
        #버튼 트리거
        self.ui.vr_count_btn.clicked.connect(self.cnt_btn_click)#카운트버튼 트리거
        self.ui.vr_save_pressure_btn.setCheckable(True) #녹화버튼 관련 환경 트리거
        self.ui.vr_save_pressure_btn.clicked.connect(self.rec_btn_click) #녹화버튼 트리거
        self.ui.vr_count_excel_btn.clicked.connect(self.convert_exl) #엑셀변환 버튼
        self.ui.vr_count_reset_btn.clicked.connect(self.update_env) #카운트리셋 버튼 
        self.ui.vr_reset_pressure_btn.clicked.connect(self.pressure_btn_click) #압력 리셋 버튼 
        self.ui.pushButton.clicked.connect(self.get_selected_address) #주소 적용 버튼 
        #히트맵
        self.plot_widget = pg.PlotWidget(self.ui.vr_heatmap)
        self.plot_widget.setAspectLocked(False)
        x_range = (1, 13)
        y_range = (0.5, 7.5)
        self.plot_widget.getPlotItem().setXRange(*x_range)
        self.plot_widget.getPlotItem().setYRange(*y_range)
        self.color= [
                        [0, 0, 255], [0, 36, 218], [0, 72, 182], [0, 109, 145], [0, 145, 109], 
                        [0, 182, 72], [0, 218, 36], [0, 255, 0], [0, 255, 0], [36, 255, 0], 
                        [72, 255, 0], [109, 255, 0], [145, 255, 0], [182, 255, 0], [218, 255, 0], 
                        [255, 255, 0], [255, 255, 0], [255, 242, 0], [255, 229, 0], [255, 216, 0], 
                        [255, 203, 0], [255, 190, 0], [255, 177, 0], [255, 165, 0], [255, 165, 0], 
                        [255, 141, 0], [255, 117, 0], [255, 94, 0], [255, 70, 0], [255, 47, 0], 
                        [255, 23, 0], [255, 0, 0]
                    ]
        self.cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 32), color=self.color)
        self.heatmap = pg.ImageItem()
        self.vbox = QVBoxLayout()
        self.heatmap.setLookupTable(self.cmap.getLookupTable())
        self.plot_widget.addItem(self.heatmap)
        self.vbox.addWidget(self.plot_widget)
        self.ui.vr_heatmap.setLayout(self.vbox)
        self.timer = QTimer()
        #체크박스 관련 히트맵 
        self.check_address = [[8,9,10,11,12,13,14],[1,2,3,4,5,6,7]]
        self.selected_check_address = []
        self.checkboxes = []
        for i in range(1, 15):
            checkbox_name = f"checkBox_{i}"
            checkbox = getattr(self.ui, checkbox_name)
            self.checkboxes.append(checkbox)
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(self.checkbox_changed)
        #엑셀설정
        self.excel = None
        #실험환경 텍스트 공유
        self.env_text = TextModel()
        self.patient_text = TextModel()
        self.kg_text = TextModel()

        self.ui.vr_exp_text_edit.textChanged.connect(self.env_text.textChanged)
        self.ui.vr_env_name.textChanged.connect(self.env_text.textChanged)
        self.ui.vr_pname_text_edit.textChanged.connect(self.patient_text.textChanged)
        self.ui.vr_patient_name.textChanged.connect(self.patient_text.textChanged)
        self.ui.vr_kg_text_edit.textChanged.connect(self.kg_text.textChanged)
        self.ui.vr_patient_weight.textChanged.connect(self.kg_text.textChanged)

        self.env_text.textChanged.connect(self.update_env_text)
        self.patient_text.textChanged.connect(self.update_patient_text)
        self.kg_text.textChanged.connect(self.update_weight_text)
        #최초 환경 생성
        self.is_new_env = True
        self.setting_btn(False)
        #비프음
        self.beep = QSound("./beep.wav")
        
    
    def get_selected_address(self):
        set_address(True)
        return self.selected_check_address
    
    def checkbox_changed(self,state):
        set_address(False)
        sender = self.sender()
        for i, cb in enumerate(self.checkboxes):
            if cb == sender:
                index = i
                #print(f"Found checkbox: {index}, State: {state}")
                break

        if index is None:
            return  # 선택된 체크박스가 없을 때 

        #ui위치가 아니라 리스트 주소를 뜻함
        #address = self.check_address[index // len(self.check_address[0])][index % len(self.check_address[0])]

        if state == 2:  # 체크박스에 체크가 됐을때
            self.selected_check_address.append(index)
        else:  # Unchecked
            self.selected_check_address.remove(index)
        set_selected_checkbox(self.selected_check_address)
        
    
    #히트맵 그리는 시작 타이머
    def start_timer(self):
        self.timer.timeout.connect(self.update_heatmap)
        self.timer.start(TIME)
    
    #히트맵 끝내는 타이머
    def stop_timer(self):
        self.timer.stop()

    def update_heatmap(self):
        global g_data_dict
        #히트맵 위젯 생성
        dict_data = g_data_dict

        if len(dict_data) > 0:
            #guide_data = np.zeros((7*2,7*2))
            guide_data = np.zeros((7*2,7*2))
            for i in range(len(self.check_address)):
                for j in range(len(self.check_address[i])):
                    address = self.check_address[i][j]
                    if address in dict_data:
                        # 각 셀에 대한 인덱스 계산
                        row_start = i * 4
                        row_end = (i + 1) * 4
                        col_start = j * 2
                        col_end = (j + 1) * 2
                        # data_dict에서 주어진 주소에 해당하는 데이터를 가져옴
                        data_ = dict_data[address]
                        guide_data[col_start:col_end, row_start:row_end] = data_                      

            #self.heatmap.clear()
            self.heatmap.setImage(guide_data)
            self.heatmap.setLevels([H_MIN,H_MAX])
            self.setting_btn(True)

    #압력리셋버튼
    def pressure_btn_click(self):
        global is_pressure_reset
        is_pressure_reset = True

    #카운트버튼과 카운트 리셋버튼 제어 함수 
    def cnt_btn_click(self):
        global is_cnt
        global is_reset
        is_cnt = True
        is_reset = False
        self.beep.play()
        self.first_env()
    
    @pyqtSlot(bool)
    def rec_btn_click(self,state):#녹화버튼
        global is_rec
        self.ui.vr_save_pressure_btn.setText({True:"중지!",False:"녹화!"}[state])
        is_rec = state
        if is_rec:
            self.first_env()
    
    def first_env(self):#처음 환경 정보 
        if self.is_new_env:
            self.is_new_env = False
            title = self.ui.vr_exp_text_edit.text() if self.ui.vr_exp_text_edit.text() else self.db.messagebox('info','경고','실험명은 꼭 입력해주세요') 
            patient = self.ui.vr_pname_text_edit.text() if self.ui.vr_pname_text_edit.text() else self.db.messagebox('info','경고','환자명은 꼭 입력해주세요')
            kg = float(self.ui.vr_kg_text_edit.text()) if self.ui.vr_kg_text_edit.text() else self.db.messagebox('info','경고','무게를 꼭 입력해주세요') 

            exp_name = self.ui.vr_user_name.text() if self.ui.vr_user_name.text() else "이윤"
            p_age = int(self.ui.vr_patient_age.text()) if self.ui.vr_patient_age.text() else None
            p_gender = self.ui.vr_patient_gender.text() if self.ui.vr_patient_gender.text() else None
            p_tall = float(self.ui.vr_patient_tall.text()) if self.ui.vr_patient_tall.text() else None
            p_info = self.ui.vr_patient_info.toPlainText() if self.ui.vr_patient_info.toPlainText() else None

            self.db.save_env(title,exp_name,p_info,patient,p_tall,p_age,p_gender,kg)
    
    def update_env(self):#버튼에 따라 갱신되는 환경 정보 
        global is_reset
        
        if self.is_new_env == False:
            is_reset = True
            set_counting(0)
            title = self.ui.vr_exp_text_edit.text() if self.ui.vr_exp_text_edit.text() else self.db.messagebox('info','경고','실험명은 꼭 입력해주세요') 
            patient = self.ui.vr_pname_text_edit.text() if self.ui.vr_pname_text_edit.text()  else self.db.messagebox('info','경고','환자명은 꼭 입력해주세요')
            kg = float(self.ui.vr_kg_text_edit.text()) if self.ui.vr_kg_text_edit.text() else self.db.messagebox('info','경고','무게를 꼭 입력해주세요') 

            exp_name = self.ui.vr_user_name.text() if self.ui.vr_user_name.text() else "이윤"
            p_age = int(self.ui.vr_patient_age.text()) if self.ui.vr_patient_age.text() else None
            p_gender = self.ui.vr_patient_gender.text() if self.ui.vr_patient_gender.text() else None
            p_tall = float(self.ui.vr_patient_tall.text()) if self.ui.vr_patient_tall.text() else None
            p_info = self.ui.vr_patient_info.toPlainText() if self.ui.vr_patient_info.toPlainText() else None

            self.db.save_env(title,exp_name,p_info,patient,p_tall,p_age,p_gender,kg)
            
    def setting_data(self, data_dict):
        global g_data_dict
        g_data_dict = data_dict
    
    def convert_exl(self):
        if self.excel is not None:
            self.excel.close()
        self.excel = excel_pop_widget()
        self.excel.show()

    @pyqtSlot(str)
    def update_env_text(self, text):
        self.ui.vr_exp_text_edit.setText(text)
        self.ui.vr_env_name.setText(text)
    
    @pyqtSlot(str)
    def update_patient_text(self, text):
        self.ui.vr_pname_text_edit.setText(text)
        self.ui.vr_patient_name.setText(text)
    
    @pyqtSlot(str)
    def update_weight_text(self, text):
        self.ui.vr_kg_text_edit.setText(text)
        self.ui.vr_patient_weight.setText(text)
    
    def setting_btn(self,bool):#버튼 활성화 비활성화 설정
        self.ui.vr_count_btn.setEnabled(bool)
        self.ui.vr_save_pressure_btn.setEnabled(bool)
        self.ui.vr_count_reset_btn.setEnabled(bool)
        self.ui.vr_reset_pressure_btn.setEnabled(bool)

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot,pyqtSignal
#텍스트 공유 클래스
class TextModel(QObject):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit(self._text)


