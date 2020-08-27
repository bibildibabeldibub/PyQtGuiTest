
from PyQt5.QtCore import QPoint, QThreadPool
from PyQt5.QtGui import QPolygon
from pathlib import Path
from Player import *
import VoronoiFunction
from side_methods import animation, layoutBuilder
from Widgets import MyScene
import json
import time
import PyQt5.QtCore
from os import listdir
from os.path import isfile, join
from screeninfo import get_monitors



dict_players: [player] = []
dict_opponents: [player] = []
voronoi_lines = []
myPath = Path(__file__).absolute().parent / 'strats'

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulator")
        with open('config.json') as config_file:
            data = json.load(config_file)
            self.fps = data['aufrufe-pro-sekunde']

        self.scene = MyScene.SoccerScene(self.fps, self)
        print(type(self.scene))
        self.scene.setSceneRect(-450, -300, 900, 600)

        print(get_monitors()[0].width)
        self.animationRunning = False
        self.field = [[-450, -300], [-450, 300], [450, 300], [450, -300]]

        if get_monitors()[0] == None:
            monitor_width = 0
        else:
            monitor_width = get_monitors()[0].width

        if monitor_width != 0 and monitor_width < 1920:
            self.init_small()
        elif monitor_width != 0 and monitor_width >= 1920:
            self.init_big()
        else:
            print("Screen width = 0 ?? How u display this?")

        field_poly = QPolygonF(QPolygon([QPoint(self.field[0][0], self.field[0][1]), QPoint(self.field[1][0], self.field[1][1]),
                 QPoint(self.field[2][0], self.field[2][1]), QPoint(self.field[3][0], self.field[3][1])]))
        self.scene.addPolygon(field_poly)

        start_formation_path = 'StartFormations/'
        "load all startpositions"
        startpositions = []
        for f in listdir(start_formation_path):
            if isfile(join(start_formation_path, f)):
                startpositions.append(f)
                self.start_selector.addItem(f)

    def init_small(self):
        """Creating the main window, with several buttons and the field simulator for small screens"""
        horizontallayout = layoutBuilder.buildSmall(self)
        self.setLayout(horizontallayout)

    def init_big(self):
        """Creating the main window, with several buttons and the field simulator for huge screens """
        self.setLayout(layoutBuilder.buildBig(self))

    def scene_change(self):
        self.vor()

    def click_function(self):
        """test function for buttpn clickking"""
        self.delete_all_players()

    def close_function(self):
        """closes the window"""
        print("\n exit button has been activated\n")
        exit()

    def resizeEvent(self, event):
        """acting while window is resized"""

    def selectionchange(self, i):
        print(i)
        print(self.start_selector.currentText())
        self.load_function("StartFormations/" + self.start_selector.currentText())
        return

    def add_player(self, position=(0, 0)):
        """adds a player to scene"""
        p = player(len(dict_players)+1, False, self.scene)
        dict_players.append(p)
        self.infoPlayer.appendPlayer(p)
        self.group_pl_layout.addWidget(p.check_box)
        p.ellipse.s.positionMove.connect(self.update_info)
        print(dict_players)

    def add_opponent(self, event):
        """adds a opponent to scene"""
        op = player(len(dict_opponents) + 1, True, self.scene)
        self.infoOpponents.appendPlayer(op)
        dict_opponents.append(op)
        self.group_op_layout.addWidget(op.check_box)
        op.ellipse.s.positionMove.connect(self.update_info)

    def save_function(self, event):
        """starts file dialog for saving the player positions"""
        filenames = QFileDialog.getSaveFileName(self, 'Save File', str(myPath))
        if filenames[0] is not '':
            f = open(filenames[0], 'w')
            txt = ""
            for p in dict_players:
                txt += str(p)
            txt += "Opponents:\n"
            for x in dict_opponents:
                txt += str(x) + "\n"
            print('\n' + txt)
            f.write(txt)
            f.close()

    def load_function(self, file = None):
        """deleting actual players, starts file dialog for loading player positions"""
        if(not file):
            dialog = QMessageBox()
            dialog.setWindowTitle("Strategy deleting")
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText("Continuing will delete actual strategy")
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            val = dialog.exec_()
        else: val = 1023

        print(file)

        if val == 1024:
            filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))
        elif val == 1023: filenames = [file]
        else: return

        self.delete_all_players()
        if filenames[0] is not '':
            f = open(filenames[0], 'r')
            txt = f.read()
            if txt == '':
                return
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
                    self.group_pl_layout.addWidget(p.check_box)
                    dict_players.append(p)
                    self.infoPlayer.appendPlayer(p)
                    print(dict_players)
                    p.ellipse.s.positionMove.connect(self.update_info)

            print("\nopponents: \n")
            opponents = teams[1].split("\n")
            for wert_tripel in opponents:
                if len(wert_tripel) > 1:
                    att = wert_tripel.split(', ')
                    print("attributes:\n")
                    print(att)
                    o = player(int(att[0]), True, self.scene)
                    dict_opponents.append(o)
                    self.group_op_layout.addWidget(o.check_box)
                    o.setLocation(int(att[1]), int(att[2]))
                    self.infoOpponents.appendPlayer(o)
                    o.ellipse.s.positionMove.connect(self.update_info)
            print(dict_opponents)

    def vor(self):
        for p in dict_opponents + dict_players:
            p.polygon.setPolygon(QPolygonF())           ##clearing the polygons

        VoronoiFunction.voronoi_function(dict_players, dict_opponents, self.field)

    def update_info(self):
        """is triggered everytime a player changes his position"""

        self.vor()
        self.infoPlayer.updateInfo()
        self.infoOpponents.updateInfo()

    def add_lines(self):
        #Helferlinien
        if self.toggleLines.isChecked():
            self.helpX = self.scene.addLine(0,-300,0,300)
            self.helpY = self.scene.addLine(-450,0,450,0)
        else:
            self.scene.removeItem(self.helpX)
            self.scene.removeItem(self.helpY)

    def delete_all_players(self):

        for op in dict_opponents:
            op.check_box.setParent(None)
            self.infoOpponents.removePlayerInfo(op)
            op.__del__()
            # self.infoOpponents.removeInfo(op)
        for p in dict_players:
            p.check_box.setParent(None)
            self.infoPlayer.removePlayerInfo(p)
            p.__del__()

        dict_opponents.clear()
        dict_players.clear()

    def animation(self):
        if not self.animationRunning:
            print(type(self.scene))
            self.scene.start_animation()
            self.animationRunning = True
        else:
            self.scene.stop_animation()
            self.animationRunning = False

    def reset(self):
        self.phase = 0
        self.animationRunning = False
        self.load_function("StartFormations/" + self.start_selector.currentText())

    def anzeigen(self):
        """shows the main window"""
        self.showMaximized()
        self.raise_()
