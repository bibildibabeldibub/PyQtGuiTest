from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QBrush, QPen
from pathlib import Path

dict_players = {}
dict_opponents = {}
myPath = Path(__file__).absolute().parent / 'strats'

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        """Creating the main window, with several buttons and the field simulator"""

        blackPen = QPen(Qt.black)
        blackBrush = QBrush(Qt.black)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 900, 600)
        field = self.scene.addRect(0, 0, 900, 600, blackPen, QBrush(Qt.white))

        view = QGraphicsView(self.scene, self)
        view.setGeometry(200, 50, 1000, 700)

        self.resize(1600, 800)
        self.move(200, 100)
        self.setWindowTitle("Simulator")

        self.addplayer = QPushButton('add player', self)
        self.addplayer.move(30, 30)
        self.addplayer.clicked.connect(self.AddPlayer)

        self.addopponent = QPushButton('add opponent', self)
        self.addopponent.move(30, 60)
        self.addopponent.clicked.connect(self.AddOpponent)

        self.posbut = QPushButton("Get Position", self)
        self.posbut.move(30, 90)
        self.posbut.clicked.connect(self.click_function)

        self.closeButton = QPushButton('Exit', self)
        self.closeButton.move(900, 550)
        self.closeButton.clicked.connect(self.close_function)

        self.textbox = QLineEdit(self)
        self.textbox.move(self.width() - 350, 50)
        self.textbox.resize(300, 20)
        ##self.textbox.setText(str(self.scene.width()) + ", " + str(self.scene.height()))
        ##self.textbox.setText(str(self.player.scenePos()))

        self.saveButton = QPushButton('save strat', self)
        self.saveButton.move(30, 120)
        self.saveButton.clicked.connect(self.save_function)

        self.loadButton = QPushButton('load strat', self)
        self.loadButton.move(30, 150)
        self.loadButton.clicked.connect(self.load_function)


        self.setMinimumSize(1600, 800)

    def click_function(self):
        """test function for buttpn clickking"""
        print("button clicked")
        print(str(self.height()) + "\n" + str(self.width()) + "\n" + str(self.pos()))
        self.position = self.player.scenePos()
        x = self.position.x()
        y = self.position.y()
        print(str(x) + ", " + str(y))

    def close_function(self):
        """closes the window"""
        print("\n exit button has been activated\n")
        exit()

    def resizeEvent(self, event):
        """acting while window is resized"""
        self.closeButton.move(self.width() - 100, self.height() - 50)
        ##self.addplayer.move(self.width() / 2 - self.addplayer.width() / 2, self.height() / 2 - self.addplayer.height() / 2)
        ##self.textbox.move(self.width() - self.textbox.width()-50, 50)
        ##self.textbox.setText(str(self.size()))

    def add_player(self, event):
        """adds a player to scene"""
        if len(dict_players) == 0:
            dict_players[1] = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.black), QBrush(Qt.black))
            dict_players[1].setFlag(QGraphicsItem.ItemIsMovable)
            dict_players[1].setToolTip(str(1))
        else:
            i = sorted(dict_players.keys())[-1]+1
            dict_players[i] = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.black), QBrush(Qt.black))
            dict_players[i].setFlag(QGraphicsItem.ItemIsMovable)
            dict_players[i].setToolTip(str(i))

    def add_opponent(self, event):
        """adds a opponent to scene"""
        if len(dict_opponents) == 0:
            dict_opponents[1] = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.blue), QBrush(Qt.blue))
            dict_opponents[1].setFlag(QGraphicsItem.ItemIsMovable)
            dict_opponents[1].setToolTip(str(1))
        else:
            i = sorted(dict_opponents.keys())[-1]+1
            dict_opponents[i] = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.blue), QBrush(Qt.blue))
            dict_opponents[i].setFlag(QGraphicsItem.ItemIsMovable)
            dict_opponents[i].setToolTip(str(i))

    def save_function(self, event):
        """starts file dialog for saving the player positions"""
        filenames = QFileDialog.getSaveFileName(self, 'Save File', str(myPath))
        if filenames:
            f = open(filenames[0], 'w')
            txt = ""
            for key in dict_players.keys():
                txt += str(key) + "," + str(int(dict_players[key].x())) + "," + str(int(dict_players[key].y())) + "\n"
            txt += "Opponents:\n"
            for x in dict_opponents.keys():
                txt += str(x) + "," + str(int(dict_opponents[x].x())) + "," + str(int(dict_opponents[x].y())) + "\n"
            print(txt)
            f.write(txt)
            f.close()

    def load_function(self):
        """starts file dialog for loading player positions"""
        dict_opponents.clear()
        dict_players.clear()
        filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))
        if filenames:
            f = open(filenames[0], 'r')
            txt = f.read()
            teams = txt.split("Opponents:\n")
            print(teams[0])
            mates = teams[0].split("\n")
            for x in mates:
                if len(x) > 1:
                    att = x.split(",")
                    print("attributes:\n")
                    print(att)
                    dict_players[int(att[0])] = self.scene.addEllipse(int(att[1]), int(att[2]), 20, 20, QPen(Qt.black), QBrush(Qt.black))
                    dict_players[int(att[0])].setFlag(QGraphicsItem.ItemIsMovable)
                    dict_players[int(att[0])].setToolTip(str(att[0]))

            print("\nopponents: \n")
            opponents = teams[1].split("\n")
            for op in opponents:
                if len(op) > 1:
                    att = op.split(",")
                    print("attributes:\n")
                    print(att)
                    dict_opponents[int(att[0])] = self.scene.addEllipse(int(att[1]), int(att[2]), 20, 20, QPen(Qt.blue), QBrush(Qt.blue))
                    dict_opponents[int(att[0])].setFlag(QGraphicsItem.ItemIsMovable)
                    dict_opponents[int(att[0])].setToolTip(att[0])

    def anzeigen(self):
        """shows the main window"""
        self.show()


