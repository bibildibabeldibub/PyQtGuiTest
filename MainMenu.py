
from PyQt5.QtCore import QPoint, QThreadPool
from PyQt5.QtGui import QPolygon
from pathlib import Path
from Player import *
import VoronoiFunction
from Widgets import MyScene
from Widgets.InfoBox import InfoBox
import json
import time
import PyQt5.QtCore
from os import listdir
from os.path import isfile, join
from screeninfo import get_monitors
from datetime import datetime
import os, shutil
from side_methods import SetupToString, Logging, animation, layoutBuilder




myPath = Path(__file__).absolute().parent / 'strats'

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulator")

        self.dict_defenders: [Player] = []
        self.dict_attackers: [Player] = []
        self.voronoi_lines = []

        self.field = [[-450, -300], [-450, 300], [450, 300], [450, -300]]

        with open('config.json') as config_file:
            data = json.load(config_file)
            self.fps = data['aufrufe-pro-sekunde']
            self.repetition = data['simulation-wiederholungen']
            self.positionierungszeit = data['positionierungszeit']
            self.animationszeit= data['animationszeit']

        print(get_monitors()[0].width)
        self.animationRunning = False

        self.scene = MyScene.SoccerScene(self.fps, self.field, self)
        self.scene.setSceneRect(-450, -300, 900, 600)

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

        start_formation_path = 'StartFormations/'
        "load all startpositions"
        startpositions = []
        for f in listdir(start_formation_path):
            if isfile(join(start_formation_path, f)):
                startpositions.append(f)
                self.start_selector.addItem(f)

        self.temppath="log/temp/"
        self.t = None
        self.log = False




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
        self.close()

    def resizeEvent(self, event):
        """acting while window is resized"""

    def selectionchange(self, i):
        print(i)
        print(self.start_selector.currentText())
        self.delete_all_players()
        self.load_function("StartFormations/" + self.start_selector.currentText())
        return

    def addAttacker(self, number=None, x=None, y=None):
        """adds a player to scene"""
        if not number:
            number = len(self.dict_attackers) + 1
        offensePlayer(number, self.scene, x, y)

    def addDefender(self, number=None, x=None, y=None):
        """adds a opponent to scene"""
        if not number:
            number = len(self.dict_defenders) + 1
        defensePlayer(number, self.scene, x, y)

    def appendPlayer(self, player):
        if isinstance(player, offensePlayer):
            self.dict_attackers.append(player)
            self.infoAttackers.appendPlayer(player)
            self.group_pl_layout.addWidget(player.check_box)
        elif isinstance(player, defensePlayer):
            self.infoDefenders.appendPlayer(player)
            self.dict_defenders.append(player)
            self.group_op_layout.addWidget(player.check_box)
        player.ellipse.s.positionMove.connect(self.update_info)

    def save_function(self, event):
        """starts file dialog for saving the player positions"""
        filenames = QFileDialog.getSaveFileName(self, 'Save File', str(myPath))

        if filenames[0] is not '':
            f = open(filenames[0], 'w')
            txt = SetupToString.getString(self.dict_defenders, self.dict_attackers)
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
                    print("P" + str(len(self.dict_defenders)) + " attributes:\n")
                    print(att)
                    self.addAttacker(int(att[0]), float(att[1]), float(att[2]))

            print("\nopponents: \n")
            opponents = teams[1].split("\n")
            for wert_tripel in opponents:
                if len(wert_tripel) > 1:
                    att = wert_tripel.split(', ')
                    print("attributes:\n")
                    print(att)
                    self.addDefender(int(att[0]), float(att[1]), float(att[2]))
            print(self.dict_attackers)

    def vor(self):
        for p in self.dict_attackers + self.dict_defenders:
            p.polygon.setPolygon(QPolygonF())           ##clearing the polygons

        VoronoiFunction.voronoi_function(self.dict_defenders, self.dict_attackers, self.field)

    def update_info(self):
        """is triggered everytime a player changes his position"""

        self.vor()
        self.infoAttackers.updateInfo()
        self.infoDefenders.updateInfo()

    def add_lines(self):
        #Helferlinien
        if self.toggleLines.isChecked():
            self.scene.show_raster()
            self.helpX = self.scene.addLine(0,-300,0,300)
            self.helpY = self.scene.addLine(-450,0,450,0)

        else:
            self.scene.removeItem(self.helpX)
            self.scene.removeItem(self.helpY)
            self.scene.hide_raster()

    def delete_all_players(self):
        for op in self.dict_attackers:
            op.check_box.setParent(None)
            self.infoDefenders.removePlayerInfo(op)
            op.__del__()
        for p in self.dict_defenders:
            p.check_box.setParent(None)
            self.infoAttackers.removePlayerInfo(p)
            p.__del__()

        self.dict_attackers.clear()
        self.dict_defenders.clear()

    def animation(self, wiederholungen=0):
        self.infoAttackers.toggleEvaluation()
        self.infoDefenders.toggleEvaluation()

        self.t = datetime.now()

        if not self.resetButton.isEnabled():
            self.resetButton.setEnabled(True)

        if not self.animationRunning:
            print(type(self.scene))
            self.scene.startAnimation(self.positionierungszeit, self.animationszeit, wiederholungen)
            self.animationRunning = True
        else:
            self.scene.stopAnimation()
            self.animationRunning = False

    def startExperiment(self):
        self.log = True
        self.animation(self.repetition)

    def testSet(self):
        # dialog = QMessageBox()
        # dialog.setWindowTitle("Strategy deleting")
        # dialog.setIcon(QMessageBox.Warning)
        # dialog.setText("Continuing will delete actual strategy")
        # dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # val = dialog.exec_()
        #
        # if val == 1024:
        #     filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))
        #
        # else:
        #     exit(619)

        self.delete_all_players()
        self.scene.testSet()


    def simulationFinished(self):
        #shutil.move(self.temppath+self.date, "log/ergebnis/" + self.date)
        self.infoAttackers.toggleEvaluation()
        self.infoDefenders.toggleEvaluation()

    def saveSetup(self, situation="", wiederholung=0):
        Logging.writeLog(self, situation, wiederholung)

    def createResetPoint(self):
        """ safes Setup to reset"""
        if not self.log:
            return
        if not os.path.exists("temp"):
            os.mkdir("temp")
        if not os.path.exists("temp/resetfile"):
            os.mkdir("temp/resetfile")
        r = open("temp/resetfile/"+self.date, 'w')
        r.write(SetupToString.getString(self.dict_defenders, self.dict_attackers))

    def reset(self):
        print("--------Reset--------")
        self.delete_all_players()
        if os.path.isfile("temp/resetfile/" + self.date):
            self.load_function("temp/resetfile/" + self.date)
        else:
            print("Warning: tempfile does not exist!")
            exit()


    def anzeigen(self):
        """shows the main window"""
        self.showMaximized()
        self.raise_()

    def closeEvent(self, QCloseEvent):
        # if not os.path.exists("log/ergebnis"):
        #     os.mkdir("log/ergebnis")
        # if os.path.isfile(self.temppath+self.date):
        #     os.renames("log/temp/" + self.date, "log/ergebnis/" + self.date)

        # delete reset
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        super()
