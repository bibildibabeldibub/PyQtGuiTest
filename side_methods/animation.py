from PyQt5 import QtCore, QtWidgets
import time


class anim_worker(QtCore.QRunnable):
    def __init__(self, scene, seconds):
        QtCore.QRunnable.__init__(self)
        self.scene = scene
        self.seconds = seconds
        self.pause = False

    def run(self):
        self.loop()

    def loop(self):
        while not self.pause:
            self.scene.advance()
            time.sleep(self.seconds)

