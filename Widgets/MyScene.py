from side_methods import animation
import time
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Widgets import Aufstellung
import json
import math
from Widgets import MyEllipse
import side_methods.Bewertung
from Widgets.Aufstellung import TestSetUp
from side_methods import Bewertung

class SoccerScene(QGraphicsScene):

    stopSignal = pyqtSignal()
    continueSignal = pyqtSignal()
    positionedSignal = pyqtSignal()
    resetSignal = pyqtSignal(str)
    naivPositionCheck = pyqtSignal()

    def __init__(self, fps, field, window=None):
        super().__init__()
        self.naiv_positioned_defenders = []
        self.window = window
        with open('config.json') as config_file:
            data = json.load(config_file)
            self.reps = data['simulation-wiederholungen']
            self.t_pos = data['positionierungszeit']
            self.t_move = data['animationszeit']
            self.setup_total = data['setups']

        self.refreshDate()
        self.repetition_counter = 0
        self.phase = 0
        self.attackers = []
        self.defenders = []
        self.covered_attackers = []
        self.fps = fps
        self.animationRunning = False
        self.phase = 0
        self.advance_counter = 0
        self.threadpool = QThreadPool()
        self.animationWorker = None
        self.raster_polygons = []
        self.unordered_raster = []
        self.raster = self.rasterize()
        self.field = field
        self.setup = None
        self.setup_count = 0
        self.strat_count = 0
        self.strats = []
        self.compare = False
        self.defend_positions = []
        self.bewerter = Bewertung.Bewerter()
        self.naiv = False

        field_poly = QPolygonF(QPolygon([QPoint(self.field[0][0], self.field[0][1]), QPoint(self.field[1][0], self.field[1][1]), QPoint(self.field[2][0], self.field[2][1]), QPoint(self.field[3][0], self.field[3][1])]))
        self.addPolygon(field_poly, QPen(Qt.black))
        goal_att_poly = QPolygonF(QPolygon([QPoint(-450, -75), QPoint(-450, 75), QPoint(-475, 75), QPoint(-475, -75)]))
        goal_def_poly = QPolygonF(QPolygon([QPoint(450, -75), QPoint(450, 75), QPoint(475, 75), QPoint(475, -75)]))
        self.addPolygon(goal_att_poly, QPen(Qt.black))
        self.addPolygon(goal_def_poly, QPen(Qt.black))

    def addAttacker(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.attackers.append(player)
            self.window.appendPlayer(player)

    def addDefender(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.defenders.append(player)
            player.naivPosition.connect(self.naivPositionIncrement)
            self.window.appendPlayer(player)

    def naivPositionIncrement(self):
        print("Positioning incrementing" + str(self.sender()))
        self.naiv_positioned_defenders.append(self.sender())

    def advance(self):
        self.animation_control()
        self.advance_counter += 1
        super().advance()

    def get_advance_counter(self):
        return self.advance_counter

    def animation_control(self):
        """Steuert die Animation mit verschiedenen Phasen:
        *Phase 0 - Positionierung der Spieler
        *Phase 1 - Das eigentliche Spiel
        *Phase 1 wird unter verschiedenen Bedingungen beendet"""
        #eine Sekunde= frames/aufrufe pro sekunde => frames = t*(fps)

        if self.phase == 0 and self.advance_counter == self.getSteps(self.t_pos):
            # self.animationRunning = False
            # self.animationWorker.pause = True
            self.stopAnimation()
            self.killAnimation()
            if not self.naiv:
                while len(self.naiv_positioned_defenders) < 4:
                    time.sleep(0.5)
            self.naivPositionCheck.emit()
            self.advance_counter = 0

            self.positionedSignal.emit()
            self.naiv_positioned_defenders = []
            if self.naiv:
                self.phase = 1
            self.naiv = True
            self.restartAnimation()
            return

        if self.phase == 1 and self.advance_counter >= self.getSteps(self.t_move):
            """ Nach Abschluss der Simulationszeit
            * Speichern des Ergebnisses
            * zurücksetzen der Aufstellung
            * zurücksetzen des Advancecounters
            * Neustart des Angriffes"""
            print("Wiederholung #" + str(self.repetition_counter)+" abgeschlossen.")

            self.stopAnimation()
            self.killAnimation()

            self.naiv = False

            time.sleep(2)
            self.repetition_counter += 1

            print(self.attackers)
            self.setup.evaluateAll()
            self.setup.writeLog()
            print(self.attackers)

            time.sleep(1)

            if self.repetition_counter < self.reps:
                """ Aufstellung braucht noch durchläufe
                * Zurücksetzen der Spieler
                * Neustart der Simulation
                """

                self.resetSignal.emit("")
                self.restartAnimation()
            else:
                """Wiederholungen einer Aufstellung sind abgeschlossen
                * Neustart mit komplett neuer Aufstellung oder mit neuer Strategie
                """

                if self.compare:
                    """Neustart der Aufstellung mit anderer Strategie"""
                    print("Vergleichmodus aktiv")
                    print(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))

                    if self.strat_count < 1:
                        print("Ändere Strategie")
                        self.resetSignal.emit("Strat")
                        self.covered_attackers = []
                        self.strat_count += 1
                        self.loadDefPositions(self.strats[self.strat_count])
                        self.setup.changeStrategy()
                        self.phase = 0
                        self.repetition_counter = 0

                    elif self.setup_count < self.setup_total:
                        """Start mit neuer Aufstellung
                        * Strategie wird im Setup constructor wieder zurückgesetzt
                        """

                        self.loadDefPositions(self.strats[0])
                        self.resetSetup()

                    else:
                        """Fertig"""
                        print("Fertig!")

                        self.advance_counter = 0
                        self.phase = 0
                        self.repetition_counter = 0
                        self.strat_count = 0

                        return

                else:
                    print("Ohne Vergelcih")
                    if self.setup_count <= self.setup_total:
                        """Neue Aufstellung"""
                        print("Reset")
                        self.resetSetup()
                    else:
                        print("Test fertig")
                        self.advance_counter = 0
                        self.phase = 0
                        self.repetition_counter = 0
                        self.strat_count = 0
                        return

                self.restartAnimation()

    def getPhase(self):
        return self.phase

    def getSteps(self, seconds):
        """

        :param seconds: Sekunden, die in Schritte umgerechnet werden sollen.
        :return: Anzahl der Schritte
        """
        return self.fps * seconds

    def startAnimation(self):
        self.repetition_counter = 0
        self.advance_counter = 0
        if not self.animationRunning:
            self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)
            self.animationWorker.sender.advanceSignal.connect(self.advance)
            print("Start animation in Scene")

            self.animationRunning = True
            self.threadpool.start(self.animationWorker)

    def restartAnimation(self):
        print("Restart Animation")
        self.advance_counter = 0
        self.naiv_positioned_defenders = []

        if self.animationRunning:
            self.stopAnimation()
            self.killAnimation()

        self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)
        self.animationWorker.sender.advanceSignal.connect(self.advance)

        self.animationRunning = True
        self.threadpool.start(self.animationWorker)

    def stopAnimation(self):
        print("Stop animation")
        self.stopSignal.emit()
        self.animationRunning = False

    def continueAnimation(self):
        print("continue Animation")
        self.continueSignal.emit()
        self.animationRunning = True

    def killAnimation(self):
        if self.animationWorker:
            self.animationWorker.kill()

    def rasterize(self):
        """:returns 2D-Array von Mittelpunkten des Rasters"""
        raster = []
        raster_groesse = 10   #10 Pixel = 10 cm = 1 dm
        rh = int(raster_groesse/2)
        for i in range(0, int(600/raster_groesse)):
            raster.append([])
            for j in range(0, int(900/10)):
                raster[i].append([j*raster_groesse+rh-450, i*raster_groesse+rh-300])
                self.unordered_raster.append([j*raster_groesse+rh-450, i*raster_groesse+rh-300])


        for i in range(len(raster)):
            for j in range(len(raster[i])):
                p = QPolygonF(QRectF(raster[i][j][0]-rh, raster[i][j][1]-rh, raster_groesse, raster_groesse))
                self.raster_polygons.append(p)

        return raster

    def showRaster(self):
        self.shown_raster = []
        color = QColor(255,0,0)
        for i in self.raster_polygons:
            rp = self.addPolygon(i)

            farbwert = self.bewerter.evaluatePoint(i.boundingRect().x() + 5, i.boundingRect().y() + 5)
            if farbwert > 1:
                farbwert = 1
            color.setAlphaF(farbwert)
            rp.setPen(Qt.transparent)
            rp.setBrush(color)
            rp.update()
            self.shown_raster.append(rp)
        return

    def hide_raster(self):
        for i in self.shown_raster:
            self.removeItem(i)

    def testSet(self, compare: bool):
        self.refreshDate()
        self.setup = TestSetUp(self)
        file = self.strats[0]
        file = file.split('.')
        file = file[0]
        self.setup.changeStrategy()
        self.compare = compare
        self.startAnimation()

    def refreshDate(self):
        self.date = datetime.now()
        self.date = self.date.strftime("%d_%m_%Y_%H_%M_%S")

    def resetSetup(self):
        """
        * Löscht das aktuelle setup und erstellt ein neues
        * Setzt Stati zurück
        """
        self.strat_count = 0
        self.phase = 0
        self.repetition_counter = 0
        self.clearPlayers()
        # gc.collect()
        self.setup.stopBewerter()

        self.covered_attackers = []
        self.setup_count += 1
        self.setup = TestSetUp(self, self.setup_count)
        self.setup.changeStrategy()

    def clearPlayers(self):
        self.window.deleteAllPlayers()
        self.attackers.clear()
        self.defenders.clear()

    def getCurrentStrat(self):
        return self.strats[self.strat_count]

    def setStrats(self, ls=None):
        if ls:
            for x in ls:
                self.strats.append(x)
        else:
            self.strats = []

    def appendStrats(self, strat: str):
        self.loadDefPositions(strat)
        self.strats.append(strat)

    def loadDefPositions(self, strat):
        if strat.endswith('.json'):
            filename = "Strategies/"+strat
            with open(filename, 'r') as file:
                data = file.read()
            obj = json.loads(data)
            for pos in obj.keys():
                self.defend_positions.append(obj[pos])

    def bewertung(self):
        self.bewerter.evaluateScene(self)

