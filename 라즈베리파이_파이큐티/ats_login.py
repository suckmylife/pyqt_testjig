import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QWidget, QLineEdit
from PyQt5.QtGui import QIcon
#기능 모듈 
from ats_main import MainWindow
from ats_database import connectdb

#ui 파일
import neo
from qrc_login import Ui_Form

#로그인 기능
ID = None
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #아이콘 세팅
        self.icon = QIcon(":/neo/neoable.png")
        self.setWindowIcon(self.icon)
        #자동 크기 조절
        self.ui.title.setWordWrap(True)

        #메인 연결
        self.main = MainWindow()
        self.stacked_widget = self.main.stacked_widget

        #DB 연결
        self.database = connectdb()

        # 로그인 버튼 클릭 시 이벤트 연결
        self.ui.login_btn.clicked.connect(self.login)
        self.ui.id.returnPressed.connect(self.login)
        self.ui.psw.returnPressed.connect(self.login)
        self.ui.psw.setEchoMode(QLineEdit.Password)
    
    def login(self):
        psw = self.ui.psw.text()
        global ID
        ID = self.ui.id.text()
        verify = self.database.login_verify(ID,psw)
        if verify:
            self.main.show()
            self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec_()