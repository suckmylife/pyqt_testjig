# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'verson_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_version_setting(object):
    def setupUi(self, version_setting):
        version_setting.setObjectName("version_setting")
        version_setting.resize(1200, 540)
        self.label = QtWidgets.QLabel(version_setting)
        self.label.setGeometry(QtCore.QRect(200, -10, 211, 51))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(version_setting)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 210, 91, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.layoutWidget_2 = QtWidgets.QWidget(version_setting)
        self.layoutWidget_2.setGeometry(QtCore.QRect(150, 340, 91, 91))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.layoutWidget_3 = QtWidgets.QWidget(version_setting)
        self.layoutWidget_3.setGeometry(QtCore.QRect(260, 210, 181, 91))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.vs_board_ver = QtWidgets.QLabel(self.layoutWidget_3)
        self.vs_board_ver.setText("")
        self.vs_board_ver.setObjectName("vs_board_ver")
        self.verticalLayout_5.addWidget(self.vs_board_ver)
        self.vs_board_info = QtWidgets.QLabel(self.layoutWidget_3)
        self.vs_board_info.setText("")
        self.vs_board_info.setObjectName("vs_board_info")
        self.verticalLayout_5.addWidget(self.vs_board_info)
        self.vs_board_update = QtWidgets.QLabel(self.layoutWidget_3)
        self.vs_board_update.setText("")
        self.vs_board_update.setObjectName("vs_board_update")
        self.verticalLayout_5.addWidget(self.vs_board_update)
        self.layoutWidget_4 = QtWidgets.QWidget(version_setting)
        self.layoutWidget_4.setGeometry(QtCore.QRect(260, 340, 181, 91))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.vs_aircell_ver = QtWidgets.QLabel(self.layoutWidget_4)
        self.vs_aircell_ver.setText("")
        self.vs_aircell_ver.setObjectName("vs_aircell_ver")
        self.verticalLayout_6.addWidget(self.vs_aircell_ver)
        self.vs_aircell_info = QtWidgets.QLabel(self.layoutWidget_4)
        self.vs_aircell_info.setText("")
        self.vs_aircell_info.setObjectName("vs_aircell_info")
        self.verticalLayout_6.addWidget(self.vs_aircell_info)
        self.vs_aircell_update = QtWidgets.QLabel(self.layoutWidget_4)
        self.vs_aircell_update.setText("")
        self.vs_aircell_update.setObjectName("vs_aircell_update")
        self.verticalLayout_6.addWidget(self.vs_aircell_update)
        self.groupBox = QtWidgets.QGroupBox(version_setting)
        self.groupBox.setGeometry(QtCore.QRect(520, 110, 431, 251))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.apply_btn = QtWidgets.QPushButton(self.groupBox)
        self.apply_btn.setGeometry(QtCore.QRect(320, 120, 81, 51))
        self.apply_btn.setObjectName("apply_btn")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 80, 61, 121))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_7.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(100, 70, 171, 151))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.board_combo = QtWidgets.QComboBox(self.layoutWidget2)
        self.board_combo.setObjectName("board_combo")
        self.verticalLayout_8.addWidget(self.board_combo)
        self.aircell_combo = QtWidgets.QComboBox(self.layoutWidget2)
        self.aircell_combo.setObjectName("aircell_combo")
        self.verticalLayout_8.addWidget(self.aircell_combo)
        self.layoutWidget3 = QtWidgets.QWidget(version_setting)
        self.layoutWidget3.setGeometry(QtCore.QRect(150, 80, 91, 91))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.layoutWidget4 = QtWidgets.QWidget(version_setting)
        self.layoutWidget4.setGeometry(QtCore.QRect(260, 80, 181, 91))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.vs_sw_ver = QtWidgets.QLabel(self.layoutWidget4)
        self.vs_sw_ver.setText("")
        self.vs_sw_ver.setObjectName("vs_sw_ver")
        self.verticalLayout_4.addWidget(self.vs_sw_ver)
        self.vs_sw_info = QtWidgets.QLabel(self.layoutWidget4)
        self.vs_sw_info.setText("")
        self.vs_sw_info.setObjectName("vs_sw_info")
        self.verticalLayout_4.addWidget(self.vs_sw_info)
        self.vs_sw_update = QtWidgets.QLabel(self.layoutWidget4)
        self.vs_sw_update.setText("")
        self.vs_sw_update.setObjectName("vs_sw_update")
        self.verticalLayout_4.addWidget(self.vs_sw_update)

        self.retranslateUi(version_setting)
        QtCore.QMetaObject.connectSlotsByName(version_setting)

    def retranslateUi(self, version_setting):
        _translate = QtCore.QCoreApplication.translate
        version_setting.setWindowTitle(_translate("version_setting", "Form"))
        self.label.setText(_translate("version_setting", "현재 버전 정보"))
        self.label_5.setText(_translate("version_setting", "보드 :"))
        self.label_6.setText(_translate("version_setting", "내용 : "))
        self.label_7.setText(_translate("version_setting", "업데이트 : "))
        self.label_8.setText(_translate("version_setting", "에어셀 :"))
        self.label_9.setText(_translate("version_setting", "내용 : "))
        self.label_10.setText(_translate("version_setting", "업데이트 : "))
        self.groupBox.setTitle(_translate("version_setting", "버전 정보 변경"))
        self.apply_btn.setText(_translate("version_setting", "변경"))
        self.label_12.setText(_translate("version_setting", "보드 :"))
        self.label_13.setText(_translate("version_setting", "에어셀 :"))
        self.label_2.setText(_translate("version_setting", "소프트웨어 : "))
        self.label_3.setText(_translate("version_setting", "내용 : "))
        self.label_4.setText(_translate("version_setting", "업데이트 : "))
