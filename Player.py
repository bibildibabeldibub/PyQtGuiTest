from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class player:
    def __init__(self, number: int, op: bool, scene: QGraphicsScene, posx: int = None, posy: int = None):
        """initialising player with ellipse, op is boolean and should be true if the player is an opponent"""
        self.op = op
        self.number = number
        self.scene = scene
        if not posx:
            posx = 0
        if not posy:
            posy = 0
        if op:
            self.ellipse = self.scene.addEllipse(posx, posy, 20, 20, QPen(Qt.black), QBrush(Qt.black))
            self.ellipse.setToolTip("Player " + str(self.number))
            self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.ellipse = self.scene.addEllipse(posx, posy, 20, 20, QPen(Qt.blue), QBrush(Qt.blue))
            self.ellipse.setToolTip("Opponent " + str(self.number))
            self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)

    def setLocation(self, posx, posy):
        self.ellipse.move(posx, posy)

    def deleteMarker(self):
        self.scene.removeItem(self.ellipse)

    def __repr__(self):
        return str(int(self.number)) + ', ' + str(int(self.ellipse.x())) + ', ' + str(int(self.ellipse.y()))

    def __del__(self):
        self.scene.removeItem(self.ellipse)
