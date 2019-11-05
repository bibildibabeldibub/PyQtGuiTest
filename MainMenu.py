from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDir, QLineF
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from pathlib import Path
from Player import player
import VoronoiFunction

dict_players: [player] = []
dict_opponents: [player] = []
voronoi_lines = []
myPath = Path(__file__).absolute().parent / 'strats'

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init()


    def init(self):
        """Creating the main window, with several buttons and the field simulator"""
        horizontallayout = QHBoxLayout()
        verticallayout = QVBoxLayout()

        blackPen = QPen(Qt.black)
        blackBrush = QBrush(Qt.black)
        self.field = [[-450, -300], [-450, 300], [450, 300], [450, -300]]
        self.resize(1600, 800)
        self.move(200, 100)
        self.setWindowTitle("Simulator")

        self.addplayer = QPushButton('add player')
        self.addplayer.clicked.connect(self.add_player)
        verticallayout.addWidget(self.addplayer)

        self.addopponent = QPushButton('add opponent')
        self.addopponent.clicked.connect(self.add_opponent)
        verticallayout.addWidget(self.addopponent)

        self.posbut = QPushButton("test")
        self.posbut.clicked.connect(self.click_function)
        verticallayout.addWidget(self.posbut)

        self.saveButton = QPushButton('save strat')
        self.saveButton.clicked.connect(self.save_function)
        verticallayout.addWidget(self.saveButton)

        self.loadButton = QPushButton('load strat')
        self.loadButton.clicked.connect(self.load_function)
        verticallayout.addWidget(self.loadButton)

        self.voronoiButton = QPushButton('Voronoi')
        self.voronoiButton.clicked.connect(self.vor)
        verticallayout.addWidget(self.voronoiButton)

        verticallayout.addStretch(1)

        self.closeButton = QPushButton('Exit')
        self.closeButton.clicked.connect(self.close_function)
        verticallayout.addWidget(self.closeButton)

        horizontallayout.addLayout(verticallayout)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-450, -300, 900, 600)
        self.scene.addRect(-450, -300, 900, 600, blackPen, QBrush(Qt.white))
        #self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.blue), QBrush(Qt.black))
        view = QGraphicsView(self.scene, self)
        view.setGeometry(200, 50, 1000, 700)
        view.setMinimumSize(1000, 700)

        horizontallayout.addWidget(view)

        verticallayout3 = QVBoxLayout()
        self.textbox = QLineEdit(self)
        self.textbox.resize(300, 20)
        self.textbox.setMinimumSize(300, 20)
        verticallayout3.addWidget(self.textbox)

        group_pl, group_op = QGroupBox("Players"), QGroupBox("Opponents")
        self.group_pl_layout, self.group_op_layout = QVBoxLayout(), QVBoxLayout()
        group_pl.setLayout(self.group_pl_layout)
        group_op.setLayout(self.group_op_layout)
        groups_layout = QHBoxLayout()
        groups_layout.addWidget(group_pl)
        groups_layout.addWidget(group_op)
        verticallayout3.addLayout(groups_layout)

        verticallayout3.addStretch(1)
        horizontallayout.addLayout(verticallayout3)
        ##self.textbox.setText(str(self.scene.width()) + ", " + str(self.scene.height()))
        ##self.textbox.setText(str(self.player.scenePos()))

        self.setLayout(horizontallayout)

        #self.setMinimumSize(1600, 800)

    def click_function(self):
        """test function for buttpn clickking"""

        print(dict_players[0])

        ##dict_players.clear()
        #print("button clicked")
        #print(str(self.height()) + "\n" + str(self.width()) + "\n" + str(self.pos()))
        #self.position = self.player.scenePos()
        #x = self.position.x()
        #y = self.position.y()
        #print(str(x) + ", " + str(y))

    def close_function(self):
        """closes the window"""
        print("\n exit button has been activated\n")
        exit()

    def resizeEvent(self, event):
        """acting while window is resized"""
        ##self.addplayer.move(self.width() / 2 - self.addplayer.width() / 2, self.height() / 2 - self.addplayer.height() / 2)
        ##self.textbox.move(self.width() - self.textbox.width()-50, 50)
        ##self.textbox.setText(str(self.size()))

    def add_player(self, event):
        """adds a player to scene"""
        p = player(len(dict_players)+1, False, self.scene)
        dict_players.append(p)
        self.group_pl_layout.addWidget(p.check_box)
        print(dict_players)


    def add_opponent(self, event):
        """adds a opponent to scene"""
        op = player(len(dict_opponents) + 1, True, self.scene)
        dict_opponents.append(op)
        self.group_op_layout.addWidget(op.check_box)
        print(dict_opponents)


    def save_function(self, event):
        """starts file dialog for saving the player positions"""
        filenames = QFileDialog.getSaveFileName(self, 'Save File', str(myPath))
        if filenames[0] is not '':
            f = open(filenames[0], 'w')
            txt = ""
            for key in dict_players:
                txt += str(key) 
            txt += "Opponents:\n"
            for x in dict_opponents:
                txt += str(x) + "\n"
            print('\n' + txt)
            f.write(txt)
            f.close()

    def load_function(self):
        """deleting actual players, starts file dialog for loading player positions"""

        dialog = QMessageBox()
        dialog.setWindowTitle("Strategy deleting")
        dialog.setIcon(QMessageBox.Warning)
        dialog.setText("Continuing will delete actual strategy")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        val = dialog.exec_()
        print(val)

        if val == 1024:

            dict_opponents.clear()
            dict_players.clear()
            filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))

            if filenames[0] is not '':
                f = open(filenames[0], 'r')
                txt = f.read()
                teams = txt.split("Opponents:\n")
                print(teams[0])
                play_atts = teams[0].split("\n")
                for wert_tripel in play_atts:
                    if len(wert_tripel) > 1:
                        att = wert_tripel.split(", ")   # 3 attribute von einzelnen spielern
                        print("P"+str(len(dict_players)) + " attributes:\n")
                        print(att)
                        p = player(int(att[0]), False, self.scene)
                        p.setLocation(int(att[1]), int(att[2]))
                        dict_players.append(p)
                        print(dict_players)

                print("\nopponents: \n")
                opponents = teams[1].split("\n")
                for wert_tripel in opponents:
                    if len(wert_tripel) > 1:
                        att = wert_tripel.split(', ')
                        print("attributes:\n")
                        print(att)
                        o = player(int(att[0]), True, self.scene)
                        dict_opponents.append(o)
                        o.setLocation(int(att[1]), int(att[2]))
                print(dict_opponents)

    def vor(self):
        for p in dict_opponents + dict_players:
            p.polygon.setPolygon(QPolygonF())           ##clearing the polygons

        VoronoiFunction.voronoi_function(dict_players, dict_opponents, self.field)


    def anzeigen(self):
        """shows the main window"""
        self.show()


