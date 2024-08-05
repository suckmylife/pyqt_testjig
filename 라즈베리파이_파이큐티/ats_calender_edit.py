from PyQt5.QtWidgets import QApplication, QCalendarWidget,QWidget,QVBoxLayout,QPushButton,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QTextCharFormat
from PyQt5.QtCore import pyqtSignal

class Calender(QCalendarWidget):#캘린더 생성 
	def __init__(self):
		super().__init__()
		self.from_date = None
		self.to_date = None

		#캘린더에서 날짜 선택했을때 스타일 적용
		self.highlighter_format = QTextCharFormat()
		self.highlighter_format.setBackground(self.palette().brush(QPalette.Highlight))
		self.highlighter_format.setForeground(self.palette().color(QPalette.HighlightedText))

		#날짜 적용버튼 클릭시
		self.clicked.connect(self.select_range)

		super().dateTextFormat()

	#선택된 날짜 범위에 하이라이트 해주는 범위
	def highlight_range(self, format):
		if self.from_date and self.to_date:
			d1 = min(self.from_date, self.to_date)
			d2 = max(self.from_date, self.to_date)
			while d1 <= d2:
				self.setDateTextFormat(d1, format)
				d1 = d1.addDays(1)

	#쉬프트를 눌렀을때 날짜 선택하게 하는 것
	def select_range(self, date_value):
		self.highlight_range(QTextCharFormat())
		
		if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.from_date:
			self.to_date = date_value
			self.highlight_range(self.highlighter_format)
		else:
			self.from_date = date_value	
			self.to_date = None

from PyQt5.QtGui import QIcon
import neo
class EditDate(QWidget):
	data_signal = pyqtSignal(list)#적용 날짜 바뀔때마다 감지
	
	def __init__(self):
		super().__init__()
		self.icon = QIcon(":/neo/neoable.png")
		self.window_width, self.window_height = 400, 200
		self.setMinimumSize(self.window_width, self.window_height)
		self.setWindowTitle('날짜 선택')
		self.setStyleSheet('''QWidget {font-size: 15px;}''')		

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		
		self.calendar = Calender()
		btn = QPushButton('적용', clicked=self.apply_date)
		
		self.layout.addWidget(self.calendar)
		self.layout.addWidget(btn)

	#버튼을 눌렀을때 날짜를 감지하는 곳
	def apply_date(self):
		if self.calendar.from_date and self.calendar.to_date:
			start_date = min(self.calendar.from_date.toPyDate(), self.calendar.to_date.toPyDate())
			end_date = max(self.calendar.from_date.toPyDate(), self.calendar.to_date.toPyDate())
			date = [start_date,end_date]
			self.data_signal.emit(date)
		else:
			msg = QMessageBox()
			msg.setWindowTitle('안내')
			msg.setText('날짜를 선택하지 않았습니다')
			msg.setWindowIcon(self.icon)
			msg.exec_()