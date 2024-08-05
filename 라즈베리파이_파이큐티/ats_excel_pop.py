from ats_database import connectdb
from PyQt5.QtWidgets import QWidget,QItemDelegate,QLineEdit, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QApplication
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QIcon
#데이터 관련 선언
select_data = 0 #선택된 행
env_id = 0 #선택된 행의 no.
#날짜선택 담는 곳
date = []
#기능 모듈 
from ats_calender_edit import EditDate
import neo
from qrc_excel import Ui_count_to_excel

class excel_pop_widget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_count_to_excel()
        self.ui.setupUi(self)
        #아이콘 세팅
        self.icon = QIcon(":/neo/neoable.png")
        self.setWindowIcon(self.icon)
        self.box = QVBoxLayout()
        self.db = connectdb()
        self.cal = None

        self.db.call_cnt(self.ui.exl_count_list,"init")

        # 커스텀 딜리게이트 생성 및 적용
        self.setting = table_setting(self.ui.exl_count_list)
        self.ui.exl_count_list.setItemDelegate(self.setting)

        # 열의 편집 불가능 설정
        for col in range(self.ui.exl_count_list.columnCount()):
            if col == 0:  # 예시로 2번째 열(인덱스 1)을 편집 불가능하게 설정
                for row in range(self.ui.exl_count_list.rowCount()):
                    item = self.ui.exl_count_list.item(row, col)
                    if item:
                        flags = item.flags()
                        flags &= ~Qt.ItemIsEditable  # 편집 불가능하게 설정
                        item.setFlags(flags)

        self.qlines = []#qlineedit 모음

        #편집용 이벤트
        self.ui.exl_patient_name.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_name" : self.line_edit(obj_name)
        self.ui.exl_patient_age.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_age" : self.line_edit(obj_name)
        self.ui.exl_patient_gender.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_gender": self.line_edit(obj_name)
        self.ui.exl_patient_tall.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_tall": self.line_edit(obj_name)
        self.ui.exl_patient_weight.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_weight": self.line_edit(obj_name)
        self.ui.exl_patient_info.mouseDoubleClickEvent = lambda event, obj_name="exl_patient_info": self.line_edit(obj_name)

        #이벤트
        self.ui.exl_count_list.cellClicked.connect(self.table_cell_clicked)
        self.ui.exl_count_list.itemSelectionChanged.connect(self.detail)
        self.ui.exl_convert.clicked.connect(self.convert_exl)
        self.ui.exl_list_before.clicked.connect(self.paging_before)
        self.ui.exl_list_after.clicked.connect(self.paging_after)
        self.ui.exl_calen.clicked.connect(self.cal_edit)
        self.ui.exl_count_list.itemChanged.connect(self.update_cell)
        self.ui.pushButton.clicked.connect(self.refresh)
        

        #새로고침 이벤트
        self.ignore_item_change = False

    def table_cell_clicked(self,row,col):
        self.select_row(row,col)
        self.qline_hide()

    @pyqtSlot(list)#날짜 적용할때마다 실행됨
    def paging_date(self,data):
        self.ui.exl_count_list.clear()
        self.db.call_cnt(self.ui.exl_count_list,"init",data)
        global date
        date = data
    
    #다음페이지 조회 함수 
    def paging_after(self):
        global date
        self.ignore_item_change = True
        if self.ignore_item_change:
            self.ui.exl_count_list.clear()
            if len(date)>1:
                self.db.call_cnt(self.ui.exl_count_list,"next",date)
            else:
                self.db.call_cnt(self.ui.exl_count_list,"next")
            self.ignore_item_change = False

    #이전페이지 조회 함수 
    def paging_before(self):
        global date
        self.ignore_item_change = True
        if self.ignore_item_change:
            self.ui.exl_count_list.clear()
            if len(date)>1:
                self.db.call_cnt(self.ui.exl_count_list,"prev",date)
            else:
                self.db.call_cnt(self.ui.exl_count_list,"prev")
            self.ignore_item_change = False
    
    #세부항목 조회 함수 
    def detail(self):
        select = self.ui.exl_count_list.selectedItems()
        if len(select) > 1 :
            global select_data
            global env_id
            env_id = int(select[0].text()) #no.
            select_data = select[2].text() #date
            self.db.call_cnt_info(self.ui,env_id)
    
    #행 선택 함수 
    def select_row(self,row,column):
        self.ui.exl_count_list.selectRow(row)
    
    #카운트 데이터 엑셀변환 함수 
    def convert_exl(self):
        global select_data
        global env_id
        if select_data:
            self.db.convert_exl(select_data,env_id)
    
    #날짜 검색 함수
    def cal_edit(self):
        if self.cal is not None:
            self.cal.close()
        self.cal = EditDate()
        self.cal.show()
        self.cal.data_signal.connect(self.paging_date)
    
    #셀 편집 함수 
    def update_cell(self,item):
        if self.ignore_item_change == False:
            global env_id
            global date
            text = item.text()
            self.db.edit_update(text,env_id)
    #새로고침 함수 
    def refresh(self):
        self.ignore_item_change = True
        if self.ignore_item_change:
            global date
            self.db.call_cnt(self.ui.exl_count_list,"init",date)
            self.ignore_item_change = False

    #세부항목 편집할때 qlineedit에 대한 제어 함수 
    def qline_hide(self):
        if self.qlines:
            for line in self.qlines:
                line.hide()
    
    #세부항목 편집에 대한 UI 제어 함수 
    def line_edit(self,obj_name):
        self.qline_hide()
        label = getattr(self.ui,obj_name)
        text = label.text()
        rect = label.geometry()

        qline = QLineEdit(self.ui.groupBox)
        qline.setGeometry(rect)
        qline.setText(text)
        qline.show()
        self.qlines.append(qline)
        qline.editingFinished.connect(lambda: self.detail_edit(obj_name,qline.text()))
    
    #세부항목 편집 함수 
    def detail_edit(self,label_name,text):
        global env_id
        condition = None
        if label_name == "exl_patient_name":
            condition = "patient_name"
        elif label_name == "exl_patient_age":
            condition = "patient_age"
        elif label_name == "exl_patient_gender":
            condition = "patient_gender"
        elif label_name == "exl_patient_tall":
            condition = "patient_tall"
        elif label_name == "exl_patient_weight":
            condition = "patient_weight"
        elif label_name == "exl_patient_info":
            condition = "exp_info"
        
        self.db.detail_edit_update(condition,text,env_id)
        self.detail()
        


class table_setting(QItemDelegate):
    def createEditor(self, parent, option, index):
        # 열 인덱스를 확인하여 특정 열에 대해서만 에디터를 생성하거나 생성하지 않음
        if index.column() == 2:  
            return None
        else:
            return super().createEditor(parent, option, index)

    def editorEvent(self, event, model, option, index):
        # 특정 열을 클릭하더라도 아무런 동작이 발생하지 않음
        if index.column() == 2:  
            return False
        else:
            return super().editorEvent(event, model, option, index)
