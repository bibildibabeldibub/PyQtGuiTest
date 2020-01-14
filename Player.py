from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import warnings
import numpy as np
from Widgets.MyEllipse import MyEllipse
import random


class player:
    positionChanged = pyqtSignal()
    polygonChanged = pyqtSignal()

    def __init__(self, number: int, op: bool, scene: QGraphicsScene):
        """initialising player with ellipse, op is boolean and should be true if the player is an opponent"""
        self.op = op
        self.number = number
        self.scene = scene
        self.vertices = []
        self.polygon = self.scene.addPolygon(QPolygonF(), QPen(Qt.red))
        self.removePoly()

        if op:
            string = "Opponent " + str(self.number)
            self.check_box = QCheckBox(string)
            self.check_box.toggled.connect(self.togglePoly)
            self.check_box.setChecked(True)

            self.ellipse = MyEllipse(00, 00, 20, 20, QPen(Qt.black), QBrush(Qt.black), self.scene)
            self.ellipse.setPos(20, 20)
            self.ellipse.setToolTip(string)

        else:
            string = "Player " + str(self.number)
            self.check_box = QCheckBox(string)
            self.check_box.toggled.connect(self.togglePoly)
            self.check_box.setChecked(True)

            self.ellipse = MyEllipse(0, 0, 20, 20, QPen(Qt.blue), QBrush(Qt.blue), self.scene)
            self.ellipse.setToolTip(string)
        self.check_box.setToolTip("Toggle Polygon display")

    def setLocation(self, posx, posy):
        self.ellipse.setPos(posx, posy)

    def getLocation(self):
        """:return: tuple x and y coordinates as integer"""
        return [self.ellipse.scenePos().x(), self.ellipse.scenePos().y()]

    def getLocationArray(self):
        return np.array([[self.ellipse.scenePos().x(), self.ellipse.scenePos().y()]])

    def deleteMarker(self):
        self.scene.removeItem(self.ellipse)

    def removePoly(self):
        self.scene.removeItem(self.polygon)

    def togglePoly(self):
        cb = self.check_box
        if cb.isChecked():
            self.scene.addItem(self.polygon)
        else:
            self.removePoly()

    def area(self):
        pls = []
        pol = self.polygon.polygon()
        for p in range(pol.count()):
            pls.append([pol[p].x(), pol[p].y()])
        erg = 0
        for k in range(pol.count()):            ##2A
            if k+1 < pol.count():
                pkt1X = pol[k].x()+450               ##umrechnen der punkte, damit das ergebnis positiv ist
                pkt2X = pol[k+1].x()+450
                pkt1Y = pol[k].y()+300
                pkt2Y = pol[k+1].y()+300
                erg += ((pkt1X * pkt2Y) - (pkt1Y * pkt2X))
            else:
                pkt1X = pol[k].x() + 450  ##umrechnen der punkte, damit das ergebnis positiv ist
                pkt2X = pol[0].x() + 450
                pkt1Y = pol[k].y() + 300
                pkt2Y = pol[0].y() + 300
                erg += ((pkt1X * pkt2Y) - (pkt1Y * pkt2X))

        return abs(.5*erg/10000)                        ##umrechnung in Quadratmeter

    def setPoly(self, points):
        self.vertices = points
        polyF = QPolygonF()

        for p in points:
            polyF.append(QPointF(p[0], p[1]))

        self.polygon.setPolygon(polyF)

    def posChange(self):
        self.positionChanged.emit()

    def __repr__(self):
        return str(int(self.number)) + ', ' + str(int(self.ellipse.x())) + ', ' + str(int(self.ellipse.y())) + '\n'

    def __del__(self):
        print("DESTRUCTION")
        self.scene.removeItem(self.ellipse)
        self.scene.removeItem(self.polygon)
