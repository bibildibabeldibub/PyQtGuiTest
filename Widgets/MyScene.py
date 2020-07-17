
from side_methods import animation
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Widgets import MyEllipse


class SoccerScene(QGraphicsScene):

    stopSignal = pyqtSignal()

    def __init__(self, fps, window=None):
        super().__init__()
        self.window = window
        self.advance_counter = 0
        self.phase = 0
        self.attackers = []
        self.defenders = []
        self.fps = fps
        self.animationRunning = False
        self.phase = 0
        self.advance_counter = 0
        self.threadpool = QThreadPool()
        self.animationWorker = None

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
