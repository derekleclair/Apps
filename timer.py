import sys
import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QLCDNumber, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, QSize, Qt
from PySide6.QtGui import QIntValidator


class Timer(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setFixedSize(QSize(600,450)) 


        self.total_seconds = 0
        self.lcd = TimerDisplay()
        self.update_display()

        self.hours_edit = QLineEdit()
        self.hours_edit.setPlaceholderText("00")
        self.hours_edit.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.hours_label = QLabel()
        self.hours_label.adjustSize()
        self.hours_label.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Preferred)


        self.minutes_edit = QLineEdit()
        self.minutes_edit.setPlaceholderText("00")
        self.minutes_edit.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.minutes_label = QLabel()
        self.minutes_label.adjustSize()
        self.minutes_label.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Preferred)


        self.seconds_edit = QLineEdit()
        self.seconds_edit.setPlaceholderText("00")
        self.seconds_edit.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.seconds_label = QLabel()
        self.seconds_label.adjustSize()
        self.seconds_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)


        self.start_button = QPushButton()
        self.start_button.setText("Start")
        self.pause_button = QPushButton()
        self.pause_button.setText("Pause")
        self.stop_button = QPushButton()
        self.stop_button.setText("Stop")
        self.repeat_button = QPushButton()
        self.repeat_button.setText("Repeat")
        self.hours = 0
        self.minutes = 0
        self.seconds = 0


        time_edit_layout = QHBoxLayout()
        time_edit_layout.addWidget(self.hours_label, alignment=Qt.AlignmentFlag.AlignHCenter) 
        time_edit_layout.addWidget(self.hours_edit,  alignment=Qt.AlignmentFlag.AlignHCenter) 
        time_edit_layout.addWidget(self.minutes_label,  alignment=Qt.AlignmentFlag.AlignHCenter)
        time_edit_layout.addWidget(self.minutes_edit,  alignment=Qt.AlignmentFlag.AlignHCenter)
        time_edit_layout.addWidget(self.seconds_label,  alignment=Qt.AlignmentFlag.AlignHCenter)
        time_edit_layout.addWidget(self.seconds_edit,  alignment=Qt.AlignmentFlag.AlignHCenter)


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button,  alignment=Qt.AlignmentFlag.AlignHCenter)
        button_layout.addWidget(self.pause_button,  alignment=Qt.AlignmentFlag.AlignHCenter)
        button_layout.addWidget(self.stop_button,  alignment=Qt.AlignmentFlag.AlignHCenter)
        button_layout.addWidget(self.repeat_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0,0,0,0) 


        validator = QIntValidator(1, 59, self)
        hours_validator = QIntValidator(1, 99, self)
        self.minutes_edit.setValidator(validator)
        self.seconds_edit.setValidator(validator)
        self.hours_edit.setValidator(hours_validator)


        self.hours_label.setText("Hours: ")
        self.minutes_label.setText("Minutes: ")
        self.seconds_label.setText("Seconds: ")
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.lcd)
        main_layout.addLayout(time_edit_layout)
        main_layout.addLayout(button_layout)
        container.setLayout(main_layout)


        self.timer = QTimer()
        self.setCentralWidget(container) 

        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.repeat_button.clicked.connect(self.repeat_timer)
        self.timer.timeout.connect(self.count_update)


    def start_timer(self):
        if self.total_seconds == 0:
            self.hours = int(self.hours_edit.text() or 0)
            self.minutes = int(self.minutes_edit.text() or 0)
            self.seconds = int(self.seconds_edit.text() or 0)
            self.total_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds

#stored_timer used when repeating
            self.stored_timer = self.total_seconds

            self.hours_edit.setText("")
            self.minutes_edit.setText("")
            self.seconds_edit.setText("")
            
            if self.total_seconds > 0:
                self.update_display()
                self.timer.start(1000)
        elif self.total_seconds != 0:
            if self.total_seconds > 0:
                self.update_display()
                self.timer.start(1000)


    def pause_timer(self):
        self.timer.stop()

        
    def stop_timer(self):
        self.total_seconds = 0
        self.timer.stop()
        self.update_display()

    def repeat_timer(self):
        self.total_seconds = self.stored_timer
        self.update_display()

    def count_update(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1
            self.update_display()
        else:
            self.timer.stop()



    def update_display(self):
        hours, remainder = divmod(self.total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")

class TimerDisplay(QLCDNumber):
    def __init__(self):
        super().__init__()
        self.setDigitCount(8)


app = QApplication(sys.argv)
with open("style.qss", "r") as f:
    style = f.read()
app.setStyleSheet(style)
window = Timer()
window.show()
app.exec()
