
from side_methods import animation
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
from Widgets import MyEllipse


class SoccerScene(QGraphicsScene):

    stopSignal = pyqtSignal()

    def __init__(self, fps, window=None):
        super().__init__()
        self.window = window
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

        with open('config.json') as config_file:
            data = json.load(config_file)
            self.fps = data['aufrufe-pro-sekunde']

    def advance(self):
        self.animation_control()
        self.advance_counter += 1
        super().advance()

    def add_attacker(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.attackers.append(player)

    def add_defender(self, player):
        if player not in self.defenders and player not in self.attackers:
            self.defenders.append(player)

    def get_advance_counter(self):
        return self.advance_counter

    def animation_control(self):
        """Steuert die Animation mit verschiedenen Phasen:
        *Phase 0 - Positionierung der Spieler
        *Phase 1 - Das eigentliche Spiel
        *Phase 1 wird unter verschiedenen Bedingungen beendet"""
        #eine Sekunde= frames/aufrufe pro sekunde => frames = t*(fps)
        if self.advance_counter == self.fps*45:     #Phase 0 nach 45 Sekunden beendet
            self.animationRunning = False
            self.animationWorker.pause = True
            self.phase = 1
            print("Pause")
            time.sleep(3) ##Pause zwischen Phasen
            self.animationRunning = True
            self.animationWorker.pause = False

    def start_animation(self):
        if not self.animationRunning:
            self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)
            self.animationWorker.sender.advanceSignal.connect(self.advance)
            print("Start animation in Scene")

            self.animationRunning = True
            self.threadpool.start(self.animationWorker)

    def stop_animation(self):
        print("Stop animation")
        self.stopSignal.emit()
        self.animationWorker.pause = True
        self.animationRunning = False

    def kill_animation(self):
        self.animationWorker = animation.anim_worker(self.window, self, 1/self.fps)

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

