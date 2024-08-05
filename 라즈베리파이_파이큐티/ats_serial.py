
# Serial 설정과 동작을 관리하는 모듈

import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QGridLayout,QLabel,QComboBox,QGroupBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,QThread,QObject, QTimer
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo
from PyQt5.QtCore import QWaitCondition,QMutex,QByteArray,QIODevice
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QPushButton,QTextEdit
import time

__platform__ = sys.platform

#기능 모듈 
#from visualize import visual_widget
import ats_visualize
from ats_parsing import Parsing
#펌웨어 통신용 선언
SLAVE = [] # 보드수 = 스레드 반복
COUNT = 0 # 보드수 만큼 ++ 됨
responses = [] #응답 모으기 

#메인 툴바버튼 통신
btn_serial = False
class SerialRequestWorker(QObject):
    """
    시리얼 연결이 성공하면 항상 데이터를 수신
    """
    # 사용자 정의 시그널 선언
    # 받은 데이터 그대로를 전달 해주기 위해 QByteArray 형태로 전달
    request_data = pyqtSignal(QByteArray, name="requestData")
    request_reset = pyqtSignal(QByteArray,name="requestReset")
    finished = pyqtSignal()
    no_request = pyqtSignal()
    # str 방식과 다름 

    def __init__(self, serial):
        super().__init__()
        self.cond = QWaitCondition()
        self._status = False
        self.mutex = QMutex()
        self.serial = serial
        self.requests = ['7EE7044D0181FF', '7EE7044D0281FF', '7EE7044D0381FF',
                         '7EE7044D0481FF', '7EE7044D0581FF','7EE7044D0681FF',
                         '7EE7044D0781FF','7EE7044D0881FF','7EE7044D0981FF',
                         '7EE7044D0A81FF','7EE7044D0B81FF','7EE7044D0C81FF',
                         '7EE7044D0D81FF','7EE7044D0E81FF']
        self.pressure_reset = '7EE7054D0382C7'
        

    def run(self):
        """
        들어온 데이터가 있다면 시그널을 발생
        :return:
        """
        global responses
        global SLAVE
        global COUNT
        
        self.mutex.lock()
        if not self._status:
            self.cond.wait(self.mutex)
        if len(SLAVE) >0:
            hex = self.requests[SLAVE[COUNT]]
            #COUNT += 1
            request = bytes.fromhex(hex)
            self.request_data.emit(request)

            if ats_visualize.get_reset():
                    ats_visualize.set_reset(False)
            if ats_visualize.get_p_reset():
                reset = bytes.fromhex(self.pressure_reset)
                self.request_reset.emit(reset)
                ats_visualize.set_p_reset(False)
            
            self.finished.emit()
        else:
            self.no_request.emit()
        self.mutex.unlock()

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @pyqtSlot(bool, name='setStatus')
    def set_status(self, status):
        self._status = status
        if self._status:
            self.cond.wakeAll()


class SerialResponseWorker(QObject):
    """
    시리얼 연결이 성공하면 항상 데이터를 수신
    """
    # 사용자 정의 시그널 선언
    # 받은 데이터 그대로를 전달 해주기 위해 QByteArray 형태로 전달
    response_data = pyqtSignal(QByteArray, name="receivedData")
    finished = pyqtSignal()
    
    # str 방식과 다름 

    def __init__(self, serial):
        super().__init__()
        self.cond = QWaitCondition()
        self._status = False
        self.mutex = QMutex()
        self.serial = serial
        self.request_queue = []

    def run(self):
        """
        들어온 데이터가 있다면 시그널을 발생
        :return:
        """
        global responses
        self.mutex.lock()
        if not self._status:
            self.cond.wait(self.mutex)
        
        self.read_serial_data()

        self.mutex.unlock()
    
    def read_serial_data(self):
        while True:
            #if self.serial.waitForReadyRead(500):
            if self.serial.bytesAvailable() > 0:
                response = self.serial.readAll()
                self.response_data.emit(response)
                if response and len(responses) < len(SLAVE):
                    responses.append(response.toHex())
                    self.finished.emit()
                    break
            else:
                # 응답이 오지 않으면 스레드를 종료
                self.finished.emit()
                break

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @pyqtSlot(bool, name='setStatus')
    def set_status(self, status):
        self._status = status
        if self._status:
            self.cond.wakeAll()


class SerialList(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        # 시리얼통신 리스트 
        self.tree_gb = QGroupBox(self.tr("시리얼 통신 연결 리스트"))
        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabels(["포트 명","연결 상태"])
        self.tree_view.header().setVisible(True)
        self.tree_view.setAlternatingRowColors(True)

        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("공압 매트 시각화 프로그램 - 시리얼 통신")
        tlayout = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        grid_tbox = QGridLayout()

        grid_tbox.addWidget(self.tree_view)

        self.tree_gb.setLayout(grid_tbox)
      
        tlayout.addWidget(self.tree_gb)

        self.setLayout(tlayout)


class SerialController(QWidget):
    # 시리얼포트 상수 값
    BAUDRATES = (
        QSerialPort.Baud1200,
        QSerialPort.Baud2400,
        QSerialPort.Baud4800,
        QSerialPort.Baud9600,
        QSerialPort.Baud19200,
        QSerialPort.Baud38400,
        QSerialPort.Baud57600,
        QSerialPort.Baud115200,
    )

    DATABITS = (
        QSerialPort.Data5,
        QSerialPort.Data6,
        QSerialPort.Data7,
        QSerialPort.Data8,
    )

    FLOWCONTROL = (
        QSerialPort.NoFlowControl,
        QSerialPort.HardwareControl,
        QSerialPort.SoftwareControl,
    )

    PARITY = (
        QSerialPort.NoParity,
        QSerialPort.EvenParity,
        QSerialPort.OddParity,
        QSerialPort.SpaceParity,
        QSerialPort.MarkParity,
    )

    STOPBITS = (
        QSerialPort.OneStop,
        QSerialPort.OneAndHalfStop,
        QSerialPort.TwoStop,

    )

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        # 시리얼통신 연결 설정
        self.gb = QGroupBox(self.tr("시리얼통신 연결 설정"))
        self.cb_port = QComboBox()
        self.cb_baud_rate = QComboBox()
        self.cb_data_bits = QComboBox()
        self.cb_flow_control = QComboBox()
        self.cb_parity = QComboBox()
        self.cb_stop_bits = QComboBox()

        # 시리얼 인스턴스 생성
        # 시리얼 스레드 설정 및 시작
        self.serial = QSerialPort()
        self.serial_info = QSerialPortInfo()
        self.request_worker = SerialRequestWorker(self.serial)
        self.response_worker = SerialResponseWorker(self.serial)

        # 요청 스레드 초기화
        self.request_thread = QThread()
        self.request_worker.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_worker.run)
       
        # 응답 스레드 초기화
        self.response_thread = QThread()
        self.response_worker.moveToThread(self.response_thread)
        self.response_thread.started.connect(self.response_worker.run)
        
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("공압 매트 시각화 프로그램 - 시리얼 통신")
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        grid_box = QGridLayout()

        grid_box.addWidget(QLabel(self.tr("Port")), 0, 0)
        grid_box.addWidget(self.cb_port, 0, 1)

        grid_box.addWidget(QLabel(self.tr("Baud Rate")), 1, 0)
        grid_box.addWidget(self.cb_baud_rate, 1, 1)

        grid_box.addWidget(QLabel(self.tr("Data Bits")), 2, 0)
        grid_box.addWidget(self.cb_data_bits, 2, 1)

        grid_box.addWidget(QLabel(self.tr("Flow Control")), 3, 0)
        grid_box.addWidget(self.cb_flow_control, 3, 1)

        grid_box.addWidget(QLabel(self.tr("Parity")), 4, 0)
        grid_box.addWidget(self.cb_parity, 4, 1)

        grid_box.addWidget(QLabel(self.tr("Stop Bits")), 5, 0)
        grid_box.addWidget(self.cb_stop_bits, 5, 1)

        self._fill_serial_info()

        self.gb.setLayout(grid_box)

        layout.addWidget(self.gb)

        self.setLayout(layout)

    def _fill_serial_info(self):
        # 시리얼 상수 값들을 위젯에 채운다
        self.cb_port.insertItems(0, self._get_available_port())
        self.cb_baud_rate.insertItems(0, [str(x) for x in self.BAUDRATES])
        self.cb_data_bits.insertItems(0, [str(x) for x in self.DATABITS])
        flow_name = {0: "None", 1: "Hardware", 2: "Software"}
        self.cb_flow_control.insertItems(0, [flow_name[x] for x in self.FLOWCONTROL])
        parity_name = {0: "None", 2: "Even", 3: "Odd", 4: "Space", 5: "Mark"}
        self.cb_parity.insertItems(0, [parity_name[x] for x in self.PARITY])
        stop_bits_name = {1: "1", 3: "1.5", 2: "2"}
        self.cb_stop_bits.insertItems(0, [stop_bits_name[x] for x in self.STOPBITS])

    def refresh_port(self):
        self.cb_port.clear()
        self.cb_port.insertItems(0, self._get_available_port())

    @staticmethod
    def get_port_path():
        """
        현재플래폼에 맞게 경로 또는 지정어를 반환
        :return:
        """
        return {"linux": '/dev/ttyS', "win32": 'COM'}[__platform__]

    def _get_available_port(self):
        """
        255개의 포트를 열고 닫으면서 사용가능한 포트를 찾아서 반환
        :return:
        """
        available_port = list()
        port_path = self.get_port_path()

        for number in range(255):
            port_name = port_path + str(number)
            if not self._open(port_name):
                continue
            available_port.append(port_name)
            self.serial.close()
        return available_port

    def _open(self, port_name, baudrate=QSerialPort.Baud38400, data_bits=QSerialPort.Data8,
              flow_control=QSerialPort.NoFlowControl, parity=QSerialPort.NoParity, stop_bits=QSerialPort.OneStop):
        info = QSerialPortInfo(port_name)
        self.serial.setPort(info)
        self.serial.setBaudRate(baudrate)
        self.serial.setDataBits(data_bits)
        self.serial.setFlowControl(flow_control)
        self.serial.setParity(parity)
        self.serial.setStopBits(stop_bits)
        return self.serial.open(QIODevice.ReadWrite)

    def connect_serial(self):
        serial_info = {
            "port_name": self.cb_port.currentText(),
            "baudrate": self.BAUDRATES[self.cb_baud_rate.currentIndex()],
            "data_bits": self.DATABITS[self.cb_data_bits.currentIndex()],
            "flow_control": self.FLOWCONTROL[self.cb_flow_control.currentIndex()],
            "parity": self.PARITY[self.cb_parity.currentIndex()],
            "stop_bits": self.STOPBITS[self.cb_stop_bits.currentIndex()],
        }
        status = self._open(**serial_info)
        #포트 연결
        self.request_worker.setStatus(status)
        self.response_worker.setStatus(status)
        return status

    def disconnect_serial(self):
        return self.serial.close()

    @pyqtSlot(bytes, name="writeData")
    def write_data(self, data):
        self.serial.writeData(data)


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.te = QTextEdit()
        self.pb = QPushButton("연결")
        self.pb_send = QPushButton("포트새로고침")
        self.serial = SerialController()
        self.treeview = SerialList()
        self.parse = Parsing()
        self.init_widget()

        self.timer = None

        self.serial.request_worker.request_data.connect(self.send_request)
        #self.serial.request_worker.request_reset.connect(self.send_request)
        self.serial.response_worker.response_data.connect(self.receive_response)
        self.serial.request_worker.finished.connect(self.serial.response_thread.start)
        self.serial.response_worker.finished.connect(self.response_worker_finished)
        self.serial.request_worker.no_request.connect(self.end_workers)

        
    def init_widget(self):
        self.setWindowTitle("공압 매트 시각화 프로그램 - 시리얼통신")
        self.serial.setGeometry(900,40,221,261)
        self.pb.setGeometry(910,310,91,23)
        self.pb_send.setGeometry(1010,310,101,23)
        self.treeview.setGeometry(30,40,451,291)

        self.pb.clicked.connect(self.slot_clicked_connect_button)
        self.pb_send.clicked.connect(self.serial.refresh_port)
        
        self.serial.setParent(self)
        self.pb.setParent(self)
        self.pb_send.setParent(self)
        self.treeview.setParent(self)
        # 많이 사용하는 옵션을 미리 지정해 둔다.
        # 38400 8N1
        self.serial.cb_baud_rate.setCurrentIndex(5)
        self.serial.cb_data_bits.setCurrentIndex(3)

    def start_workers(self):
        if self.serial.serial.isOpen():
            self.timer = QTimer()
            self.timer.timeout.connect(self.thread_working)
            self.timer.start(500)
    
    def thread_working(self):
        if btn_serial == False and ats_visualize.get_address():
            global SLAVE
            global COUNT
            if ats_visualize.get_address():
                    SLAVE = ats_visualize.get_selected_checkbox()
            if len(SLAVE)>0:
                self.serial.response_thread.quit()
                self.serial.response_thread.wait() 
                self.serial.request_thread.quit()
                self.serial.request_thread.wait() 

                self.serial.request_thread.start()
                #self.serial.response_thread.start()
                
                

    def end_workers(self):
        self.serial.request_thread.quit()
        self.serial.request_thread.wait()
        self.serial.response_thread.quit()
        self.serial.response_thread.wait()
        if self.timer is not None:
            self.timer.stop()
    
    def end_trigger(self,value):
        global btn_serial
        btn_serial = value
        if value:
            ats_visualize.set_address(False)

    @pyqtSlot(QByteArray)
    def send_request(self, request):
        self.serial.writeData(request)
    
    @pyqtSlot(QByteArray)
    def receive_response(self, response):
        self.serial.request_thread.quit()
        self.serial.request_thread.wait()
        global COUNT
        COUNT += 1

    @pyqtSlot()
    def response_worker_finished(self):
        global COUNT
        global SLAVE
        global responses
        global btn_serial
        
        if COUNT < len(SLAVE):
            self.start_workers()
        else:
            cntbtn = ats_visualize.get_cnt() # 카운트 버튼이 눌렸을때 트리거 함수 호출 
            recbtn = ats_visualize.get_record()
            if cntbtn:
                ats_visualize.set_cnt(False)
                self.parse.DB_cnt(responses)

            self.end_workers()
            
            #if btn_serial == False:
            if recbtn == True:
                self.parse.DB_rec(responses)
            self.parse.parse_realtime(responses)
            self.start_workers()
            COUNT = 0
            responses = []
            
                

    @pyqtSlot(name="clickedConnectButton")
    def slot_clicked_connect_button(self):
        tv = self.treeview.tree_view
        current_port = self.serial.cb_port.currentText()
        current_items = [tv.topLevelItem(i) for i in range(tv.topLevelItemCount())]
        current_item_names = [item.text(0) for item in current_items]
        
        if self.serial.serial.isOpen():
            self.serial.disconnect_serial()
            self.treeview_disconnect(tv,current_port)

        else:
            self.serial.connect_serial()
            self.treeview_connect(tv,current_port,current_item_names)
                                                 
        self.pb.setText({False: '연결', True: '연결 끊기'}[self.serial.serial.isOpen()])
    
    def treeview_connect(self,tv,cur_port,cur_list): 
        find = tv.findItems(cur_port, Qt.MatchContains)
        if cur_port not in cur_list:
            item = QTreeWidgetItem(tv)
            item.setText(0,cur_port)
            item.setText(1,"○")
            tv.addTopLevelItem(item)
        else:
            for item in find:
                item.setText(1, "○")
    
    def treeview_disconnect(self,tv,cur_port):
        find = tv.findItems(cur_port, Qt.MatchContains)
        for item in find:
            item.setText(1,"X")
            
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    excepthook = sys.excepthook
    sys.excepthook = lambda t, val, tb: excepthook(t, val, tb)
    form = Form()
    form.show()
    exit(app.exec_())