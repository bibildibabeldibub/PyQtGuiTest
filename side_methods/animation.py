from PyQt5 import QtCore, QtWidgets
import time


class anim_worker(QtCore.QRunnable):
    def __init__(self, window, scene, seconds):
        QtCore.QRunnable.__init__(self)
        self.scene = scene
        self.seconds = seconds
        self.pause = False
        self.mainWindow = window

    def run(self):
        self.loop()

    def loop(self):
        while not self.pause:
            self.scene.advance()
            self.mainWindow.animation_control()
            time.sleep(self.seconds)

