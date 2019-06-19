from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        blackPen = QPen(Qt.black)
        blackBrush = QBrush(Qt.black)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 900, 600)
        field = self.scene.addRect(0, 0, 900, 600, blackPen, QBrush(Qt.white))
        self.player = self.scene.addEllipse(0, 0, 20, 20, blackPen, blackBrush)
        self.player.setFlag(QGraphicsItem.ItemIsMovable)
        self.player.setToolTip("Player 1")
        view = QGraphicsView(self.scene, self)
        view.setGeometry(200, 50, 1000, 700)

        self.resize(1600, 800)
        self.move(200, 100)
        self.setWindowTitle("DingDongSchamalamaDINGdingDong")

        self.addplayer = QPushButton('add player', self)
        self.addplayer.move(30, 30)
        self.addplayer.clicked.connect(self.AddPlayer)

        self.posbut = QPushButton("Get Position", self)
        self.posbut.move(30, 60)
        self.posbut.clicked.connect(self.click_function)

        self.closeButton = QPushButton('Exit', self)
        self.closeButton.move(900, 550)
        self.closeButton.clicked.connect(self.close_function)

        self.textbox = QLineEdit(self)
        self.textbox.move(self.width() - 350, 50)
        self.textbox.resize(300, 20)
        ##self.textbox.setText(str(self.scene.width()) + ", " + str(self.scene.height()))
        self.textbox.setText(str(self.player.scenePos()))

        self.setMinimumSize(1600, 800)

    def click_function(self):
        print("button clicked")
        print(str(self.height()) + "\n" + str(self.width()) + "\n" + str(self.pos()))
        self.position = self.player.scenePos()
        x = self.position.x()
        y = self.position.y()
        print(str(x) + ", " + str(y))

    def close_function(self):
        print("\n exit button has been activated\n")
        exit()

    def resizeEvent(self, event):
        self.closeButton.move(self.width() - 100, self.height() - 50)
        ##self.addplayer.move(self.width() / 2 - self.addplayer.width() / 2, self.height() / 2 - self.addplayer.height() / 2)
        ##self.textbox.move(self.width() - self.textbox.width()-50, 50)
        ##self.textbox.setText(str(self.size()))

    def AddPlayer(self, event):
        newplayer = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.black), QBrush(Qt.black))
        newplayer.setFlag(QGraphicsItem.ItemIsMovable)

    def anzeigen(self):
        self.show()


