from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF, QColor
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF, QObject, pyqtSignal, pyqtSlot
import numpy as np
from Widgets.MyEllipse import MyEllipse
import json
from side_methods.bewertung import evaluate_point
import time
import math
import random


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

    def getPosRaster(self):
        """:returns mögliche Positionen des Angreifers"""
        positions = []

        radius = self.velocity * self.scene.t_move
        print(type(self))
        print(self)
        print("Create distance circle with radius= " + str(radius))
        kreis = self.scene.addEllipse(self.getLocation()[0]-radius, self.getLocation()[1]-radius, radius*2, radius*2, QPen(Qt.blue), QBrush(Qt.transparent))
        #Rasterung des Kreises in 10x10 felder
        for i in self.scene.raster:
            for j in i:
                if kreis.contains(QPointF(j[0], j[1])):
                    positions.append(j)
                    # p = QPolygonF(QRectF(j[0]-5, j[1]-5, 10, 10))
                    # self.scene.addPolygon(p,QPen(Qt.green),QBrush(Qt.transparent))

        self.scene.removeItem(kreis)
        return positions

    def setColor(self, color: QColor):
        # self.ellipse.brush = QBrush(Qt.darkGreen)
        self.ellipse.direction_pen = QPen(color)
        self.ellipse.update()

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


class offensePlayer(player):
    def __init__(self, number: int, op: bool, scene: QGraphicsScene, blocked=False):
        super().__init__(number, False, scene)

        self.blocked = blocked

        string = "Player " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.ellipse.setToolTip(string)


class defensePlayer(player):
    def __init__(self, number: int, op: bool, scene: QGraphicsScene, destination=None):
        super().__init__(number, True, scene)

        string = "Defense " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.enemy = None
        self.att_distances = {}

        self.ellipse.setBrush(QBrush(Qt.black))
        self.ellipse.setPen(QPen(Qt.black))
        self.ellipse.setToolTip(string)
        self.ellipse.setTransformOriginPoint(10,10)
        self.ellipse.setRotation(180)
        self.ellipse.update()

    def findEnemy(self, ohne: player = None):
        """:var enemy Dieser Spieler wird  ausgelassen in der Suche (Für den Fall dass nochmal gesucht werden muss)
            """
        if not self.att_distances:
            print("Generiere Distanztabelle")
            x = self.getLocation()[0]
            y = self.getLocation()[1]
            print(self.scene.attackers)

            for i in self.scene.attackers:
                #get for every attacker the distance
                dx = i.getLocation()[0] - x
                dy = i.getLocation()[1] - y
                distance = math.sqrt(dx*dx+dy*dy)
                self.att_distances.update({i:distance})

        print(self.att_distances)

        if ohne:
            self.att_distances.pop(ohne)

        while self.att_distances:
            distance_min = min(self.att_distances.values())
            possible = []
            for a,d in self.att_distances.items():
                #finde Gegner mit geringster Distanz
                if d == distance_min:
                    possible.append(a)

            for p in possible:
                print(self.scene.covered_attackers)
                if not p in self.scene.covered_attackers.keys():
                    #Spieler wird gedeckt
                    print("-----------------Erfolg!!!-----------------")
                    print(type(p))
                    self.enemy = p
                    color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.enemy.setColor(color)
                    self.setColor(color)
                    self.scene.covered_attackers.update({p: self})
                    return
                else:
                    print("Gegner bereits gedeckt")
                    mitspieler = self.scene.covered_attackers[p]
                    d2 = mitspieler.getCoveredDistance()
                    if self.att_distances[p] >= d2:
                        #Suche neuen Gegner
                        self.att_distances.pop(p)
                    else:
                        #Spieler wird gedeckt
                        self.enemy = p
                        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        self.enemy.setColor(color)
                        self.setColor(color)
                        mitspieler.findEnemy(p)
                        return

        return

    def enemyCovered(self, enemy):
        return

    def getCoveredDistance(self):
        return self.att_distances[self.enemy]

    def applyCoveredEnemyRequest(self, enemy):
        if enemy in self.covered_enemies:
            return False
        else:
            self.covered_enemies.append(enemy)
            return True

    def evalEnemyPositions(self):
        """Bewertet die Positionen des Gegners"""
        if not self.enemy:
            print("Kein Gegner gefunden!")
            return

        attacker = self.enemy
        positions = attacker.getPosRaster()
        max_val = 0
        worst_case_pos = []
        worst_case_pos_str = []
        point_val = {}
        for i in positions:
            val=evaluate_point(i[0], i[1])
            point_val.update({str(i):val})

        #Beachte Worstcase:
        max_val = max(point_val.values())
        print("Worstcase-Positionen:")
        for point, value in point_val.items():
            if value == max_val:
                worst_case_pos_str.append(point)

        for i in worst_case_pos_str:
            point = i.strip('][').split(', ')
            point[0] = int(point[0])
            point[1] = int(point[1])
            print(point)
            worst_case_pos.append(point)
            self.scene.addEllipse(point[0],point[1],10,10,QPen(Qt.red),QBrush(Qt.red))
        #Beachte Mittlere ??

        return




