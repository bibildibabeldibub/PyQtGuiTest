from PyQt5 import QtWidgets
import time

class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.advance_counter = 0
        self.phase = 0

    def advance(self):
        if self.advance_counter >= self.fps*45: #Phase 0 nach 45 Sekunden vorbei
            self.phase = 1
            time.sleep(3) ##Pause zwischen Phasen

        self.advance_counter += 1
        super().advance()


    def get_advance_counter(self):
        return self.advance_counter

    def advance_control(self):
        self.advance_counter += 1
        #eine Sekunde frames/aufrufe pro sekunde
        if self.advance_counter >= self.fps*45: #Phase 0 nach 45 Sekunden vorbei
            self.animationRunning = False
            self.phase = 1
            time.sleep(3) ##Pause zwischen Phasen
            self.animationRunning = True