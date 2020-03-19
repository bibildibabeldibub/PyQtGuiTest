from PyQt5 import QtWidgets, QtGui


class MyField(QtWidgets.QGraphicsRectItem):
    # def __init__(self):
    #     super(MyField, self).__init__()

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path
