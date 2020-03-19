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
        self.setPen(pen)
        self.setBrush(brush)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.spieler = p
        self.new_pos = [0, 0]

    def itemChange(self, change, value):
        """Habits on Movement """
        if change == QGraphicsItem.ItemPositionChange:
            #trunk_collide=[]
            #colliding_items = self.collidingItems()
            #for i in range(len(colliding_items)):
            #    if str(type(colliding_items[i])) != "<class 'PyQt5.QtWidgets.QGraphicsRectItem'>" and str(type(colliding_items[i])) != "<class 'PyQt5.QtWidgets.QGraphicsPolygonItem'>":
            #        trunk_collide.append(colliding_items[i])
            #
            #if trunk_collide:
            #    print(trunk_collide)
            #
            #else:
            #    print("CLEAR <3")
            # colliding_item = self.scene.itemAt(value.x(), value.y(), QTransform())
            # # print(colliding_item)
            # if str(type(colliding_item)) != "<class 'PyQt5.QtWidgets.QGraphicsRectItem'>" and str(type(colliding_item)) != "<class 'PyQt5.QtWidgets.QGraphicsPolygonItem'>" and colliding_item:
            #     return QPointF(self.x(), self.y())

            dummy_ellipse = QGraphicsEllipseItem(value.x(), value.y(), 20, 20)
            colliding_items = self.scene.items(dummy_ellipse.shape())
            filtered_colliding_items = [o for o in colliding_items if (not isinstance(o, QGraphicsPolygonItem) and (o is not self))]
            if filtered_colliding_items:

                print(filtered_colliding_items)
                return QPointF(self.x(), self.y())
            else: print("None")

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
                    self.richtungswinkel = random.uniform(-45, 45)
                    self.animcounter = 0
                self.new_pos = self.positionsBerechnung(self.richtungswinkel)
                print(self.new_pos)

                if(self.checkCollision(self.new_pos[0],self.new_pos[1])):
                    self.spieler.blocked = True
                #while self.checkCollision(self.new_pos[0], self.new_pos[1]):
                    #berechne winkel neu falls ein spieler an der position ist
                #    winkel = random.uniform(-45, 45)
                #    self.new_pos = self.positionsBerechnung(winkel)

        if p_int == 1 and not self.spieler.blocked:
            print("PositionSet!!" + str(self.new_pos))
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
            print(filtered_colliding_items)
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
