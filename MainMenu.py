
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
import random




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

        self.strat_path = 'Strategies/'
        "Laden der Strategien in die Selektorboxen"
        strats = []
        for f in listdir(self.strat_path):
            if isfile(join(self.strat_path, f)):
                strats.append(f)
                if f == "__init__.py":
                    continue
                self.strat_selector1.addItem(f)
                self.strat_selector2.addItem(f)

        self.examples_path = 'Beispiele'
        for f in listdir(self.examples_path):
            if isfile(join(self.examples_path, f)):
                strats.append(f)
                self.example_selector_att.addItem(f)
                self.example_selector_def.addItem(f)

        self.temppath = "log/temp/"
        self.t = None
        self.log = False
        self.comparison = False


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
        self.deleteAllPlayers()

    def close_function(self):
        """closes the window"""
        print("\n exit button has been activated\n")
        self.close()

    def resizeEvent(self, event):
        """acting while window is resized"""

    def selectionChange1(self, i):
        print(self.strat_selector1.currentText())
        return

    def selectionChange2(self, i):
        print(self.strat_selector2.currentText())
        return

    def addAttacker(self, number=None, x=None, y=None):
        """adds a player to scene"""
        if not number:
            number = len(self.dict_attackers) + 1
        if not x and x != 0:
            x = random.uniform(-450, 0)
        if not y and y != 0:
            y = random.uniform(-300, 300)
        offensePlayer(number, self.scene, x, y)

    def addDefender(self, number=None, x=None, y=None):
        """adds a opponent to scene"""
        if not number:
            number = len(self.dict_defenders) + 1
        if not x and x != 0:
            x = random.uniform(0, 450)
        if not y and y != 0:
            y = random.uniform(-300, 300)
        defensePlayer(number, self.scene, x, y)

    def appendPlayer(self, player):
        if isinstance(player, offensePlayer):
            self.dict_attackers.append(player)
            self.info_attackers.appendPlayer(player)
            self.group_pl_layout.addWidget(player.check_box)
        elif isinstance(player, defensePlayer):
            self.info_defenders.appendPlayer(player)
            self.dict_defenders.append(player)
            self.group_op_layout.addWidget(player.check_box)
        player.ellipse.s.positionMove.connect(self.vor)

    def save_function(self, event):
        """starts file dialog for saving the player positions"""
        filenames = QFileDialog.getSaveFileName(self, 'Save File', str(myPath))

        if filenames[0] is not '':
            f = open(filenames[0], 'w')
            txt = SetupToString.getString(self.dict_defenders, self.dict_attackers)
            f.write(txt)
            f.close()

    def load_function(self, file=None):
        """deleting actual players, starts file dialog for loading player positions"""
        if(not file):
            # dialog = QMessageBox()
            # dialog.setWindowTitle("Strategy deleting")
            # dialog.setIcon(QMessageBox.Warning)
            # dialog.setText("Continuing will delete actual strategy")
            # dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # val = dialog.exec_()
            val = 1024
        else: val = 1023

        print(file)

        if val == 1024:
            filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))
        elif val == 1023: filenames = [file]
        else:
            return

        self.deleteAllPlayers()
        if filenames[0] is not '':
            f = open(filenames[0], 'r')
            txt = f.read()
            jdata = json.loads(txt)
            attacker = jdata["Attacker"]
            defender = jdata["Defender"]

            for k in attacker.keys():
                self.addAttacker(int(k), attacker[k]["posx"], attacker[k]["posy"])

            print("Verteidiger:")
            for k in defender.keys():
                print(str(k) + ", " + str(defender[k]["posx"]) + ", " + str(defender[k]["posy"]))
                self.addDefender(int(k), defender[k]["posx"], defender[k]["posy"])

    def loadEndpositions(self, file=None):
        """deleting actual players, starts file dialog for loading player positions"""
        if(not file):
            filenames = QFileDialog.getOpenFileName(self, 'Save File', str(myPath))
        else:
            filenames = [file]

        input_dialog = QInputDialog()
        num, ok = QInputDialog.getInt(input_dialog, "Wiederholungsauswahl", "Zahl der Wiederholung, die angezeigt werden soll:")
        if not ok:
            exit("Fehler bei Woederholungsauswahl")

        num = "run-" + str(num)
        self.deleteAllPlayers()
        if filenames[0] is not '':
            f = open(filenames[0], 'r')
            txt = f.read()
            jdata = json.loads(txt)
            attacker = jdata["Scores"][num]["Attacker"]
            defender = jdata["Scores"][num]["Defender"]

            for k in attacker.keys():
                self.addAttacker(int(k), attacker[k]["posx"], attacker[k]["posy"])

            for k in defender.keys():
                self.addDefender(int(k), defender[k]["posx"], defender[k]["posy"])


    def vor(self):
        for p in self.dict_attackers + self.dict_defenders:
            p.polygon.setPolygon(QPolygonF())           ##clearing the polygons

        VoronoiFunction.voronoi_function(self.dict_defenders, self.dict_attackers, self.field)

    def updateInfo(self):
        """is triggered everytime a player changes his position"""
        self.info_attackers.updateInfo()
        self.info_defenders.updateInfo()

    def addLines(self):
        #Helferlinien
        if self.toggleLines.isChecked():
            self.scene.showRaster()
            self.helpX = self.scene.addLine(0,-300,0,300)
            #self.helpY = self.scene.addLine(-450,0,450,0)

        else:
            self.scene.removeItem(self.helpX)
            #self.scene.removeItem(self.helpY)
            self.scene.hide_raster()

    def deleteAllPlayers(self):
        for op in self.dict_attackers:
            op.check_box.setParent(None)
            self.info_defenders.removePlayerInfo(op)
            op.__del__()
        for p in self.dict_defenders:
            p.check_box.setParent(None)
            self.info_attackers.removePlayerInfo(p)
            p.__del__()

        self.dict_attackers.clear()
        self.dict_defenders.clear()

    def animation(self, wiederholungen=0):
        self.t = datetime.now()

        if not self.resetButton.isEnabled():
            self.resetButton.setEnabled(True)

        if not self.animationRunning:
            print(type(self.scene))
            self.scene.startAnimation()
            self.animationRunning = True
        else:
            self.scene.stopAnimation()
            self.animationRunning = False

    def startExperiment(self):
        self.log = True
        self.animation(self.repetition)

    def testSet(self):

        if self.strat_selector1.currentText() == "Strategie 1":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Strategie 1 nicht gewählt!")
            msg.setInformativeText("Bitte wählen Sie eine Strategie aus.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        if self.comparison:
            if self.strat_selector1.currentText() == self.strat_selector2.currentText():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Strategie 1 und Strategie 2 können während des Vergleichsmodus nicht identisch sein!")
                msg.setInformativeText("Bitte wählen Sie unterschiedliche Strategien oder deaktivieren Sie den Vergleichsmodus.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            elif self.strat_selector2.currentText() == "Strategie 2":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Strategie 2 nicht gewählt!")
                msg.setInformativeText("Bitte wählen Sie eine Strategie aus.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        self.scene.setStrats()
        self.scene.appendStrats(self.strat_selector1.currentText())
        self.scene.appendStrats(self.strat_selector2.currentText())
        self.deleteAllPlayers()
        self.compare.setEnabled(False)
        self.settest.setEnabled(False)
        self.strat_selector1.setEnabled(False)
        self.strat_selector2.setEnabled(False)

        self.scene.testSet(self.comparison)

    def bewerten(self):
        self.vor()
        self.scene.bewertung()
        self.updateInfo()

    def toggleCompare(self):
        self.comparison = self.compare.checkState()

    def saveSetup(self, situation="", wiederholung=0):
        Logging.writeLog(self, situation, wiederholung)

    def reset(self):
        print("--------Reset--------")
        self.deleteAllPlayers()
        if os.path.isfile("temp/resetfile/" + self.date):
            self.load_function("temp/resetfile/" + self.date)
        else:
            print("Warning: tempfile does not exist!")
            qApp.exit(0)


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

    def exampleChangeA(self):
        filename = self.example_selector_att.currentText()
        path = 'Beispiele'
        if filename == "Angreifer":
            self.deleteAllPlayers()
            return
        filename = os.path.join(path, filename)

        if filename is not '':
            f = open(filename, 'r')
            txt = f.read()
            jdata = json.loads(txt)
            striker = jdata["Sturm"]
            mid = jdata["Mittelfeld"]
            deff = jdata["Abwehr"]
            a = 0

            for k in striker.keys():
                self.addAttacker(a, striker[k]["x"], striker[k]["y"])
                a += 1

            for k in mid.keys():
                self.addAttacker(a, mid[k]["x"], mid[k]["y"])
                a += 1

            for k in deff.keys():
                self.addAttacker(a, deff[k]["x"], deff[k]["y"])
                a += 1

        return

    def exampleChangeD(self):
        filename = self.example_selector_def.currentText()
        if filename == "Verteidiger":
            self.deleteAllPlayers()
            return
        filename = os.path.join('Beispiele', filename)

        if filename is not '':
            f = open(filename, 'r')
            txt = f.read()
            jdata = json.loads(txt)
            striker = jdata["Sturm"]
            mid = jdata["Mittelfeld"]
            deff = jdata["Abwehr"]
            a = 0

            for k in striker.keys():
                self.addDefender(a, -striker[k]["x"], striker[k]["y"])
                a += 1

            for k in mid.keys():
                self.addDefender(a, -mid[k]["x"], mid[k]["y"])
                a += 1

            for k in deff.keys():
                self.addDefender(a, -deff[k]["x"], deff[k]["y"])
                a += 1

        return

    def restartFunction(self):
        print("Neustart")
        qApp.exit(-666)
