from side_methods import animation
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Widgets import Aufstellung
import json
import math
from Widgets import MyEllipse
import side_methods.Bewertung
from Widgets.Aufstellung import TestSetUp


class SoccerScene(QGraphicsScene):

    stopSignal = pyqtSignal()
    continueSignal = pyqtSignal()
    positionedSignal = pyqtSignal()
    resetSignal = pyqtSignal()

    def __init__(self, fps, field, window=None):
        super().__init__()
        self.window = window
        self.t_pos = 0
        self.t_move = 0
        self.reps = 0
        self.repetition_counter = 0
        self.phase = 0
        self.attackers = []
        self.defenders = []
        self.covered_attackers = {}
        self.fps = fps
        self.animationRunning = False
        self.phase = 0
        self.advance_counter = 0
        self.threadpool = QThreadPool()
        self.animationWorker = None
        self.raster_polygons = []
        self.unordered_raster = []
        self.raster = self.rasterize()
        self.max_bewertung = 0
        self.field = field
        self.setup = None
        self.setup_total = 10
        self.setup_count = 0

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
            self.window.appendPlayer(player)

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

        if self.phase == 0 and self.advance_counter == self.getSteps(self.t_pos):     #Phase 0 nach 45 Sekunden beendet
            # self.animationRunning = False
            # self.animationWorker.pause = True
            self.stopAnimation()
            self.killAnimation()
            self.phase = 1
            print("Pause")
            self.positionedSignal.emit()
            time.sleep(3) ##Pause zwischen Phasen
            self.restartAnimation()
            return

        if self.phase == 1 and self.advance_counter >= self.getSteps(self.t_move):
            """ Nach Abschluss der Simulationszeit
            * Speichern des Ergebnisses
            * zurücksetzen der Aufstellung
            * zurücksetzen des Advancecounters
            * Neustart des Angriffes"""
            print("Wiederholung #" + str(self.repetition_counter)+" abgeschlossen.")

            self.repetition_counter += 1
            if self.setup:
                self.setup.evaluateAll()

                self.setup.writeLog()

            if self.repetition_counter <= self.reps:
                """ Aufstellung braucht noch durchläufe
                * Zurücksetzen der Spieler
                * Neustart der Simulation
                """

                self.resetSignal.emit()
                self.restartAnimation()
            else:
                """Wiederholungen einer Aufstellung sind fertig
                * Neue Aufstellung -> falls Setup count
                * zurücksetzen des repetition counts
                * Neustarten der Simulation"""
                self.setup_count += 1
                if self.setup_count <= self.setup_total:
                    self.setup = TestSetUp(self)
                    self.repetition_counter = 0
                    self.restartAnimation()
                else:
                    print("Test fertig")





        #-------------------Datenlogging------------------- ALT
        # if self.phase==1 and self.advance_counter == self.getSteps(5):
        #     self.window.saveSetup("Nach 5 Sekunden", self.repetition_counter)
        #
        # if self.phase==1 and self.advance_counter == self.getSteps(10):
        #     self.window.saveSetup("Nach 10 Sekunden", self.repetition_counter)
        #
        # if self.phase==1 and self.advance_counter == self.getSteps(15):
        #     self.window.saveSetup("Nach 15 Sekunden", self.repetition_counter)

    def getPhase(self):
        return self.phase

    def getSteps(self, seconds):
        """

        :param seconds: Sekunden, die in Schritte umgerechnet werden sollen.
        :return: Anzahl der Schritte
        """
        return self.fps * seconds

    def startAnimation(self, t_pos, t_move, repetitions):
        self.t_move = t_move
        self.t_pos = t_pos
        self.reps = repetitions
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

        if self.animationRunning:
            self.stopAnimation()
            self.killAnimation()

        self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)
        self.animationWorker.sender.advanceSignal.connect(self.advance)
        print("Start animation in Scene")

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
            self.animationWorker.__del__()

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

    def show_raster(self):
        self.shown_raster = []
        color = QColor(255,0,0)
        for i in self.raster_polygons:
            rp = self.addPolygon(i)

            farbwert = side_methods.Bewertung.evaluatePoint(i.boundingRect().x() + 5, i.boundingRect().y() + 5)
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

    def testSet(self):
        aufstellung = TestSetUp(self)
        print(json.dumps(aufstellung.__dict__(), indent=4))
        aufstellung.writeLog()

