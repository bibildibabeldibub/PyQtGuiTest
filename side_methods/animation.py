from PyQt5 import QtCore, QtWidgets



class anim_thread(QtCore.QThread):
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        QtCore.QThread.__init__(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.loop = QtCore.QEventLoop()
        self.scene = scene

    def start(self, seconds):
        """startet einen Timer
        @:var seconds timer triggert alle x Sekunden"""

        self.timer.start(seconds*1000)
        self.processEvents()
        ret = self.loop.exec_()
        if ret == 0:
            print("Animation gestoppt")
        else:
            print("!!!! Fehler bei Animationsstop!!!")

    def stop(self):
        self.loop.exit(0)


    def timerEvent(self):
        self.scene.advance()
