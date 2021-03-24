from PyQt5 import QtCore, QtWidgets
import time
from PyQt5.QtCore import *

class SignalSender(QObject):
    advanceSignal = QtCore.pyqtSignal()
    def __init__(self):
        QObject.__init__(self)

    def sendSignal(self):
        # print("try to send signal")
        self.advanceSignal.emit()
        # print("Signal send")

class anim_worker(QtCore.QRunnable):
    advanceSignal = QtCore.pyqtSignal()
    def __init__(self, window, scene, seconds):
        QtCore.QRunnable.__init__(self)
        self.scene = scene
        self.scene.stopSignal.connect(self.stop)
        self.scene.continueSignal.connect(self.conti)
        # self.scene.startSignal.connect(self.run)
        self.seconds = seconds
        self.pause = True
        self.mainWindow = window
        self.mainWindow.pauseSignal.connect(self.toggleStop)
        self.sender = SignalSender()
        self.counter = 0
        self.killv = False

    def run(self):
        # print("start loop")
        self.pause = False
        self.loop()

    def loop(self):
        while not self.killv:
            while not self.pause:
                # self.counter += 1
                # print(self.counter)
                self.sender.sendSignal()
                time.sleep(self.seconds)

    def stop(self):
        self.pause = True

    def kill(self):
        self.pause = True
        self.killv = True

    def conti(self):
        self.pause = False

    def toggleStop(self):
        if self.pause:
            self.pause = True
        else:
            self.pause = False

    def __del__(self):
        print("Timer deleted")
        super()

    def __repr__(self):
        string = "Timer with " + str(self.seconds) + "seconds between Signals."
        return string
