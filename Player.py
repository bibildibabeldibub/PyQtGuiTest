from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from PyQt5.QtCore import Qt, QLineF
import numpy as np


class player:
    def __init__(self, number: int, op: bool, scene: QGraphicsScene):
        """initialising player with ellipse, op is boolean and should be true if the player is an opponent"""
        self.op = op
        self.number = number
        self.scene = scene
        self.polygon = self.scene.addPolygon(QPolygonF(), QPen(Qt.red))

        if op:
            self.ellipse = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.black), QBrush(Qt.black))
            self.ellipse.setToolTip("Player " + str(self.number))
            self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.ellipse = self.scene.addEllipse(0, 0, 20, 20, QPen(Qt.blue), QBrush(Qt.blue))
            self.ellipse.setToolTip("Opponent " + str(self.number))
            self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)

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

    def __repr__(self):
        return str(int(self.number)) + ', ' + str(int(self.ellipse.x())) + ', ' + str(int(self.ellipse.y()))

    def __del__(self):
        self.scene.removeItem(self.ellipse)
        self.scene.removeItem(self.polygon)
