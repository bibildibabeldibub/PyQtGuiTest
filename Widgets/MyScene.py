
from side_methods import animation
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
from Widgets import MyEllipse


class SoccerScene(QGraphicsScene):

    stopSignal = pyqtSignal()
    continueSignal = pyqtSignal()

    def __init__(self, fps, window=None):
        super().__init__()
        self.window = window
        self.t_pos = 0
        self.t_move = 0
        self.reps = 0
        self.repetition_counter = 0
        self.phase = 0
        self.attackers = []
        self.defenders = []
        self.fps = fps
        self.animationRunning = False
        self.phase = 0
        self.advance_counter = 0
        self.threadpool = QThreadPool()
        self.animationWorker = None
        self.raster_polygons = []
        self.raster = self.rasterize()

    def add_attacker(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.attackers.append(player)

    def add_defender(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.defenders.append(player)

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
        if self.phase == 0 and self.advance_counter == self.fps*self.t_pos:     #Phase 0 nach 45 Sekunden beendet
            # self.animationRunning = False
            # self.animationWorker.pause = True
            self.stop_animation()
            self.kill_animation()
            self.phase = 1
            print("Pause")
            self.window.saveSetup()
            time.sleep(3) ##Pause zwischen Phasen
            self.restartAnimation()

        if self.phase == 1 and self.advance_counter == self.fps*self.t_move:
            """ 
            * Speichern des Ergebnisses
            * zurücksetzen der Aufstellung
            * zurücksetzen des Advancecounters
            * Neustart des Angriffes"""
            print("Wiederholung #"+ str(self.repetition_counter)+" abgeschlossen.")
            self.repetition_counter += 1
            #stop nach Zeit t_move
            self.stop_animation()
            self.kill_animation()

            #Bewerte die Positionierungen -> speichern
            #setze das Spielfeld zurück
            if self.repetition_counter < self.reps:
                self.window.reset()
                time.sleep(2)
                self.restartAnimation()

            if self.repetition_counter == self.reps:
                print("Fertig :)")
                self.stop_animation()
                self.kill_animation()

    def getPhase(self):
        return self.phase

    def start_animation(self, t_pos, t_move, repetitions):
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
        if not self.animationRunning:
            self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)
            self.animationWorker.sender.advanceSignal.connect(self.advance)
            print("Start animation in Scene")

            self.animationRunning = True
            self.threadpool.start(self.animationWorker)

    def stop_animation(self):
        print("Stop animation")
        self.stopSignal.emit()
        self.animationRunning = False

    def continue_animation(self):
        print("continue Animation")
        self.continueSignal.emit()
        self.animationRunning = True

    def kill_animation(self):
        if self.animationWorker:
            self.animationWorker.__del__()

    def rasterize(self):
        raster = []
        for i in range(0, int(600/20)):
            raster.append([])
            for j in range(0, int(900/20)):
                raster[i].append([j*20+10-450, i*20+10-300])


        for i in range(len(raster)):
            for j in range(len(raster[i])):
                p = QPolygonF(QRectF(raster[i][j][0]-10, raster[i][j][1]-10, 20, 20))
                self.raster_polygons.append(p)
        return raster

    def show_raster(self):
        self.shown_raster = []
        for i in self.raster_polygons:
            self.shown_raster.append(self.addPolygon(i, QPen(Qt.darkGreen)))
        return

    def hide_raster(self):
        for i in self.shown_raster:
            self.removeItem(i)

