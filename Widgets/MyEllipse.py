from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QTransform
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import PyQt5.QtCore
import Player
import random
import math
import Simulation
from Simulation import defense as Defense

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

        self.find_enemies = True
        self.animcounter = 0

        self.richtungswinkel = 0
        scene.addItem(self)
        self.s = ItemMoveSignal()
        self.scene = scene
        self.pen = pen
        self.brush = brush
        self.direction_pen = QPen(Qt.darkYellow)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.spieler = p
        self.new_pos = [0, 0]
        self.positioned = False
        # self.setRotation(45)

    def itemChange(self, change, value):
        """Habits on Movement """

        if change == QGraphicsItem.ItemPositionChange:

            dummy_ellipse = QGraphicsEllipseItem(value.x(), value.y(), 20, 20)
            colliding_items = self.scene.items(dummy_ellipse.shape())
            filtered_colliding_items = [o for o in colliding_items if ((type(o) is not PyQt5.QtWidgets.QGraphicsPolygonItem) and (o is not self))]

            #print("Collision:\n" + str(filtered_colliding_items))

            if filtered_colliding_items:
                print("Blocked!!!!\n")
                print(filtered_colliding_items)
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
                # offense players:
                # if self.scene.phase==0:
                if self.scene.phase==1:
                    if self.animcounter == self.scene.getSteps(self.spieler.change_rotation):
                        #erste Winkelberechnung
                        self.new_pos = [0, 0]
                        self.richtungswinkel = random.uniform(-45, 45)

                        #Rotation
                        self.setTransformOriginPoint(10, 10)
                        self.setRotation(self.richtungswinkel)

                        self.animcounter = 0
                        # print("Rotation:\t" + str(self.rotation()))
                    self.new_pos = self.moveForward()
                    # print("Positionsdifferenz:\t" + str(self.new_pos))

                # """Collision detection"""
                # if(self.checkCollision(self.new_pos[0],self.new_pos[1])):
                #     self.spieler.blocked = True

            elif self.spieler.defense:
            #Defense, Players
                if self.scene.phase == 0:
                    #Positionierungsphase

                    if self.find_enemies:
                        #Initiale Positionsermittlung für Startaufstellung
                        self.find_enemies = False
                        self.spieler.findEnemy()
                        #print(self.scene.covered_attackers)
                        self.destination = self.spieler.evalEnemyPositions()
                        self.setTransformOriginPoint(10, 10)
                        a = self.getAngle(self.destination[0], self.destination[1])
                        #print(a)
                        self.setRotation(a)

                    #Movement während Positionierungsphase
                    #print("Positionierung = " + str(self.positioned))
                    if not self.positioned:
                        self.new_pos = self.moveForward(self.destination)
                    if self.positioned:
                        angle = self.getAngle(self.spieler.enemy.getLocation()[0], self.spieler.enemy.getLocation()[1])
                        self.setTransformOriginPoint(10, 10)
                        self.setRotation(angle)
                    #self.setPos(self.destination[0],self.destination[1])

                #Rotation
                # self.setTransformOriginPoint(10,10)
                # self.setRotation(self.richtungswinkel)

                # self.new_pos = self.moveForward()

        if p_int == 1 and not self.spieler.blocked:
            # print("Old Pos:\t"+ str(old_pos[0]) + " | " + str(old_pos[1]))
            # print("New Pos:\t" + str(old_pos[0]+self.new_pos[0]) + " | " + str(old_pos[1]+self.new_pos[1]))
            if not self.spieler.defense:
                #Angreifer
                if self.scene.phase==1:
                    self.setPos(old_pos[0]+self.new_pos[0], old_pos[1]+self.new_pos[1])
                    self.animcounter += 1
            else:
                #Verteidiger
                if self.scene.phase==0:
                    if not self.positioned:
                        self.setPos(old_pos[0]+self.new_pos[0], old_pos[1]+self.new_pos[1])
                        if self.getX() == self.destination[0] and self.getY() == self.destination[1]:
                            self.positioned = True
        return

    def getAngle(self, x, y):
        """
        :param x: x coordinate of destination point
        :param y: y coordinate of destination point
        :return: angle in degrees
        """

        dx = x - self.getX()
        dy = y - self.getY()
        a = 180
        if dx < 0:
            a = 180 + math.degrees(math.atan(dy/dx))
        elif dx == 0:
            if dy < 0:
                a = 90
            elif dy > 0:
                a = -90
        elif dx > 0:
            a = math.degrees(math.atan(dy/dx))

        return a

    def moveForward(self, destination:[] = None):
        """
            *:returns nextposition calculated by scenes fps, players velocity and rotation
            *:var destination Zielposition die erreicht werden soll
        """

        distance = 1/self.scene.fps * self.spieler.velocity
        new_x = math.cos(math.radians(self.rotation())) * distance
        new_y = math.sin(math.radians(self.rotation())) * distance


        if destination:
            # Check ob Ziel erreicht wird
            # print("Ziel:\t" + str(destination[0]) + " | " + str(destination[1]))
            # print("Position:\t" + str(self.getX()) + " | " + str(self.getY()))
            # print("Neu Pos:\t" + str(self.getX()+new_x) + " | " + str(self.getY()+new_y))

            if destination[0] - self.getX() < 0:
                #Bewegung nach links
                if self.getX() + new_x <= destination[0]:
                    print("X erreicht links")
                    self.positioned = True
                    return [destination[0] - self.getX(), destination[1] - self.getY()]
            if destination[0] - self.getX() > 0:
                #Bewegung nach rechts
                if self.getX() + new_x >= destination[0]:
                    print("X erreicht rechts")
                    self.positioned = True
                    return [destination[0] - self.getX(), destination[1] - self.getY()]
            if destination[0] - self.getX() == 0:
                #Bewegung nach oben/unten
                if destination[1] - self.getY() < 0:
                    #Bewegung nach oben
                    if self.getY() + new_y <= destination[1]:
                        self.positioned = True
                        return [destination[0] - self.getX(), destination[1] - self.getY()]
                elif destination[1] - self.getY() > 0:
                    #Bewegung nach unten
                    if self.getY() + new_y >= destination[1]:
                        self.positioned = True
                        return [destination[0] - self.getX(), destination[1] - self.getY()]
                else:
                    print("Keine Bewegung notwendig")
                    self.positioned = True
                    return [0,0]

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

        #Facedirection
        painter.setPen(self.direction_pen)
        self.direction_pen = painter.pen()
        self.direction_pen.setWidth(2)
        painter.setPen(self.direction_pen)
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
