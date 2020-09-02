from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import numpy as np
from Widgets.MyEllipse import MyEllipse
import json


class player:
    positionChanged = pyqtSignal()
    polygonChanged = pyqtSignal()

    def __init__(self, number: int, op: bool, scene: QGraphicsScene, blocked=False):
        """initialising player with ellipse, op is boolean and should be true if the player is an opponent"""
        self.blocked = blocked
        self.defense = op
        if self.defense:
            color=Qt.black
        else:
            color=Qt.blue
        self.number = number
        self.scene = scene
        self.enemy_player = None
        self.covered_enemies = []
        self.vertices = []
        self.polygon = self.scene.addPolygon(QPolygonF(), QPen(Qt.red))
        self.removePoly()
        self.mittlere_Bewertung = [0,0]

        self.check_box = QCheckBox()
        self.check_box.toggled.connect(self.togglePoly)
        self.check_box.setChecked(True)
        self.check_box.setToolTip("Toggle Polygon display")

        self.ellipse = MyEllipse(self, 0, 0, 20, 20, QPen(color), QBrush(color), self.scene)

        with open('config.json') as config_file:
            data = json.load(config_file)
            self.velocity = data['roboter-geschwindigkeit']
            self.change_rotation = data['richtungswechsel-periode']

        #print("Center:\t" + str(self.ellipse.getCenter())+"\n\t" + str(self.ellipse.x()) + ", " + str(self.ellipse.y()))


    def setLocation(self, posx, posy):
        self.ellipse.setPos(posx-10, posy-10)

    def getLocation(self):
        """:return: tuple x and y coordinates as integer"""
        return [self.ellipse.getX(), self.ellipse.getY()]

    def getLocationArray(self):
        return np.array([[self.ellipse.getX(), self.ellipse.getY()]])

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

        self.mittlere_Bewertung[0] += 1
        self.mittlere_Bewertung[1] += abs(.5*erg/10000)
        return abs(.5*erg/10000)                        ##umrechnung in Quadratmeter

    def setPoly(self, points):
        self.vertices = points
        polyF = QPolygonF()

        for p in points:
            polyF.append(QPointF(p[0], p[1]))

        self.polygon.setPolygon(polyF)

    def posChange(self):
        self.positionChanged.emit()

    def getRotation(self):
        return self.ellipse.rotation()

    def __repr__(self):
        string = ''
        string += str(self.number) + ', '
        string += str(self.ellipse.getX()) + ', '
        string += str(self.ellipse.getY()) + '\n'
        return string

    def __del__(self):
        print("DESTRUCTION")
        self.scene.removeItem(self.ellipse)
        self.scene.removeItem(self.polygon)


class defensePlayer(player):
    def __init__(self, number: int, op: bool, scene: QGraphicsScene, destination=None):
        super().__init__(number, True, scene)

        string = "Defense " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.ellipse.setBrush(QBrush(Qt.black))
        self.ellipse.setPen(QPen(Qt.black))
        self.ellipse.setToolTip(string)
        self.ellipse.setTransformOriginPoint(10,10)
        self.ellipse.setRotation(180)
        self.ellipse.update()

    def findEnemy(self):
        return

    def checkCoveredEnemies(self, enemy):
        return

    def applyCoveredEnemyRequest(self, enemy):
        if enemy in self.covered_enemies:
            return False
        else:
            self.covered_enemies.append(enemy)
            return True


class offensePlayer(player):
    def __init__(self, number: int, op: bool, scene: QGraphicsScene, blocked=False):
        super().__init__(number, False, scene)

        self.blocked = blocked

        string = "Player " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.ellipse.setToolTip(string)




