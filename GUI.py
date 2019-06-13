import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.resize(1000, 600)
        self.move(460, 240)
        self.setWindowTitle("DingDongSchamalamaDINGdingDong")
        self.b = QPushButton('hola',self)
        self.b.move(500, 300)
        self.b.clicked.connect(self.click_function)
        self.closeButton = QPushButton('Exit', self)
        self.closeButton.move(900, 550)
        self.closeButton.clicked.connect(self.close_function)
        self.textbox = QLineEdit(self)
        self.textbox.move(self.width()-350, 50)
        self.textbox.resize(300, 50)
        self.textbox.setText(str(self.textbox.pos()))
        self.setMinimumSize(400, 400)
        ##Feld zeichnen
        self.show()

    def click_function(self):
        print("button clicked")
        print(str(self.height())+"\n"+str(self.width())+"\n"+str(self.pos()))

    def close_function(self):
        print("\n exit button has been activated\n")
        exit()

    def resizeEvent(self, event):
        self.closeButton.move(self.width()-100, self.height()-50)
        self.b.move(self.width()/2 - self.b.width()/2, self.height()/2-self.b.height()/2)
        self.textbox.move(self.width() - self.textbox.width()-50, 50)

app = QApplication(sys.argv)
w = MainWindow()


sys.exit(app.exec_())
