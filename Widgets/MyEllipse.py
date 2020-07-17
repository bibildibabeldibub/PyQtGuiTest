from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF, QTransform
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import PyQt5.QtCore
import warnings
import numpy as np
import Player
import random
import json
import math

class ItemMoveSignal(QObject):
    positionMove = pyqtSignal()


class MyEllipse(QGraphicsEllipseItem):
    oldpos = QPointF()

    def __init__(self, p: Player, x, y, w, h, pen, brush, scene: QGraphicsScene):
        super().__init__(x, y, w, h)

        self.xs = x
        self.ys = y
        self.ws = w
        self.hs = h

        with open('config.json') as config_file:
            data = json.load(config_file)
            self.aufrufe_pro_sekunde = data['aufrufe-pro-sekunde']
            self.geschwindigkeit = data['roboter-geschwindigkeit']
            self.richtungswechselcount = data['richtungswechsel-periode']

        self.animcounter = 0
        self.richtungswinkel = 0
        print(self.aufrufe_pro_sekunde)
        scene.addItem(self)
        self.s = ItemMoveSignal()
        self.scene = scene
        self.pen = pen
        self.brush = brush

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.spieler = p
        self.new_pos = [0, 0]
        # self.setRotation(45)

    def itemChange(self, change, value):
        """Habits on Movement """

        if change == QGraphicsItem.ItemPositionChange:

            dummy_ellipse = QGraphicsEllipseItem(value.x(), value.y(), 20, 20)
            colliding_items = self.scene.items(dummy_ellipse.shape())

            filtered_colliding_items = [o for o in colliding_items if ((type(o) is not PyQt5.QtWidgets.QGraphicsPolygonItem) and (o is not self))]

            if filtered_colliding_items:
                #print(filtered_colliding_items)
                return QPointF(self.x(), self.y())

            self.s.positionMove.emit()

        return super().itemChange(change, value)

    def advance(self, p_int):
        """Animation"""
        if self.spieler.blocked:
            return

        old_pos = [self.x(), self.y()]
        if p_int == 0:
            self.new_pos = [0, 0]
            if not self.spieler.op:
                if self.animcounter == self.richtungswechselcount:
                    #erste Winkelberechnung
                    self.richtungswinkel = random.uniform(-45, 45)   #Buggy
                    print(self.getCenter())
                    self.setTransformOriginPoint(self.getCenter())
                    self.setRotation(self.richtungswinkel)
                    self.animcounter = 0

                self.new_pos = self.positionsBerechnung(self.richtungswinkel)
                #print(self.new_pos)

                # if(self.checkCollision(self.new_pos[0],self.new_pos[1])):
                #     self.spieler.blocked = True


        if p_int == 1 and not self.spieler.blocked:
            #print("PositionSet!!" + str(self.new_pos))
            if not self.spieler.op:
                self.setPos(old_pos[0]+self.new_pos[0], old_pos[1]+self.new_pos[1])
                self.animcounter += 1
        return

    def positionsBerechnung(self, winkel: float):
        distance = self.geschwindigkeit/self.aufrufe_pro_sekunde      ##25cm/s dividiert mit Aufrufe/s
        res_x = math.cos(winkel)*distance
        res_y = math.sin(winkel)*distance
        return [abs(res_x), res_y]

    def checkCollision(self, x: float, y: float):
        """checks if another player is at position"""
        dummy_ellipse = QGraphicsEllipseItem(x, y, 20, 20)
        colliding_items = self.scene.items(dummy_ellipse.shape())
        filtered_colliding_items = [o for o in colliding_items if
                                    (not isinstance(o, QGraphicsPolygonItem) and (o is not self))]
        if filtered_colliding_items:
            return True
        return False

    def keyReleaseEvent(self, event):
        if self.isSelected():
            if event.key() == Qt.Key_Up:
                self.moveBy(0,-1)
            elif event.key() == Qt.Key_Down:
                self.moveBy(0,1)
            elif event.key() == Qt.Key_Right:
                self.moveBy(1,0)
            elif event.key() == Qt.Key_Left:
                self.moveBy(-1,0)
        return

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(0, 0, self.ws, self.hs)

        painter.setBrush(Qt.black)
        painter.drawEllipse(9, 9, 2, 2)

        #Facedirection
        painter.setPen(Qt.yellow)
        pen = painter.pen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(10, 0, 20, 10)
        painter.drawLine(10, 20, 20, 10)

    def getCenter(self):
        return QPointF(self.x()+10,self.y()+10)

    def getX(self):
        return self.x() + 10

    def getY(self):
        return self.y() + 10
