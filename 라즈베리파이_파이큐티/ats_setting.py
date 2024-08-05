from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

#기능 모듈
from ats_database import connectdb
from qrc_setting import Ui_version_setting
#버전관리
BOARD_VER = None
AIRCELL_VER = None
class setting(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_version_setting()
        self.ui.setupUi(self)

        self.db = connectdb()
        self.db.call_aircell(self.ui)
        self.db.call_board(self.ui)
        self.db.call_sw(self.ui)
        self.ui.apply_btn.clicked.connect(self.verson_alter)

    

    def verson_alter(self):
        global BOARD_VER
        global AIRCELL_VER
        BOARD_VER = self.ui.board_combo.currentText()
        AIRCELL_VER = self.ui.aircell_combo.currentText()

        self.db.call_aircell(self.ui,AIRCELL_VER)
        self.db.call_board(self.ui,BOARD_VER)
