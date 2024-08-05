import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QHBoxLayout,QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QStackedWidget,QMessageBox
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtGui import QIcon

#qrc 파일
import menue
import neo
from qrc_main import Ui_MainWindow
#기능 모듈 
from ats_visualize import visual_widget
from ats_serial import Form
from ats_parsing import Parsing
from ats_setting import setting

# 메인 윈도우
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #아이콘 세팅
        self.icon = QIcon(":/neo/neoable.png")
        self.setWindowIcon(self.icon)
        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()
        # 위젯 객체 생성
        self.visual_widget = visual_widget()
        self.serial_widget = Form()
        self.parsing = Parsing()
        self.setting_widget = setting()
        # UI 파일을 QStackedWidget에 추가
        self.stacked_widget.addWidget(self.serial_widget)
        self.stacked_widget.addWidget(self.visual_widget)
        self.stacked_widget.addWidget(self.setting_widget)
        #툴바버튼과 UI버튼 연결 
        self.ui.actionconnect_serial.triggered.connect(self.show_serial_widget)
        self.ui.actionvisual.triggered.connect(self.show_visual_widget)
        self.ui.actionsetting.triggered.connect(self.show_setting_widget)
        #이코드가 있어야 화면 전환이 됨
        center = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(center)
        self.setCentralWidget(central_widget)
        #순서 지켜서 addWidget 해야함 
        center.addWidget(self.stacked_widget)

    def show_visual_widget(self):    
        # 시각화 모듈 전환시 초기화
        self.serial_widget.end_trigger(False)
        self.serial_widget.start_workers() #스레드 시작 다른 위젯에 넣지 말것
        self.visual_widget.start_timer()
        self.parsing.start_timer()
        # 시각화 모듈로 전환
        self.stacked_widget.setCurrentWidget(self.visual_widget)
        
    def show_serial_widget(self):
        #serial 통신 모듈 전환시 초기화
        self.serial_widget.end_trigger(True)
        self.visual_widget.stop_timer()
        self.visual_widget.rec_btn_click(False)
        self.parsing.stop_timer()
        #serial 통신 모듈로 전환 
        self.stacked_widget.setCurrentWidget(self.serial_widget)
    
    def show_setting_widget(self):
        #세팅모듈 전환시 초기화
        self.serial_widget.end_trigger(True)
        self.visual_widget.stop_timer()
        self.visual_widget.rec_btn_click(False)
        self.parsing.stop_timer()
        #세팅 모듈로 전환
        self.stacked_widget.setCurrentWidget(self.setting_widget)
    
    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle('안내')
        msg.setText('프로그램을 끝내시겠습니까?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setWindowIcon(self.icon)

        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
        
import os
if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling,True)
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

