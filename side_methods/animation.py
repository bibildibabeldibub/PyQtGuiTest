from PyQt5 import QtCore, QtWidgets



class anim_thread(QtCore.QThread):
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        QtCore.QThread.__init__(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.scene = scene

    def start(self, seconds):
        self.timer.start(seconds*1000)
        loop = QtCore.QEventLoop()
        loop.exec_()

    def timerEvent(self):
        self.scene.advance()
