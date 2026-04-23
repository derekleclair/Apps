import sys
from PySide6.QtWidgets import QApplication , QMainWindow, QLabel 
from PySide6.QtGui import QIcon, QFont
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tutorial")
        self.setGeometry(700,300,500,500)
        #self.setWindowIcon(QIcon("path/to/image/"))
        label = QLabel("Hello", self)
        label.setFont(QFont("Arial", 30))
        label.setGeometry(0,0,500,100)
        label.setStyleSheet("color: blue;"
                            "background-color: green;"
                            "font-style: italic;"
                            "text-decoration: underline;")

def main():
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec_())

if __name__ == "__main__":
    main()
