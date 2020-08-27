from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QTransform
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import PyQt5.QtCore
import Player
import random
import math

class ItemMoveSignal(QObject):
    positionMove = pyqtSignal()


class MyEllipse(QGraphicsEllipseItem):
    oldpos = QPointF()

    def __init__(self, p: Player, x, y, w, h, pen:QPen, brush:QBrush, scene: QGraphicsScene):
        super().__init__(x, y, w, h)

        self.xs = x
        self.ys = y
        self.ws = w
        self.hs = h

        self.animcounter = 0
        self.richtungswinkel = 0
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
            if not self.spieler.defense:
                if self.animcounter == self.spieler.change_rotation:
                    #erste Winkelberechnung
                    self.new_pos = [0, 0]
                    self.richtungswinkel = random.uniform(-45, 45)

                    #Rotation
                    self.setTransformOriginPoint(10, 10)
                    self.setRotation(self.richtungswinkel)

                    self.animcounter = 0
                    # print("Rotation:\t" + str(self.rotation()))
                    self.new_pos = self.moveForwardNextPos()
                    # print("Positionsdifferenz:\t" + str(self.new_pos))

                """Collision detection"""
                if(self.checkCollision(self.new_pos[0],self.new_pos[1])):
                    self.spieler.blocked = True

        if p_int == 1 and not self.spieler.blocked:
            # print("Old Pos:\t"+ str(old_pos[0]) + " | " + str(old_pos[1]))
            # print("New Pos:\t" + str(old_pos[0]+self.new_pos[0]) + " | " + str(old_pos[1]+self.new_pos[1]))
            if not self.spieler.defense:
                self.setPos(old_pos[0]+self.new_pos[0], old_pos[1]+self.new_pos[1])
                self.animcounter += 1
        return

    def moveForwardNextPos(self):
        """:returns nextposition calculated by scenes fps, players velocity and rotation"""
        distance = 1/self.scene.fps * self.spieler.velocity
        new_x = math.cos(math.radians(self.rotation())) * distance
        new_y = math.sin(math.radians(self.rotation())) * distance
        return [round(new_x,2), round(new_y,2)]

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
        print("Center:\t" + str(self.x()+10) + " | " + str(self.y()+10) )
        return QPointF(self.x()+10,self.y()+10)

    def getX(self):
        """:return x value of circles center"""
        return self.x() + 10

    def getY(self):
        """:returns y value of circles center"""
        return self.y() + 10
