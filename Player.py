from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF, QColor
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF, QObject, pyqtSignal, pyqtSlot
import numpy as np
from Widgets.MyEllipse import MyEllipse
import json
from side_methods.Bewertung import evaluatePoint
import time
import math
import random


class Player:
    positionChanged = pyqtSignal()
    polygonChanged = pyqtSignal()

    def __init__(self, number: int, op: bool, scene: QGraphicsScene, posx, posy, blocked=False):
        """initialising player with ellipse, op is boolean and should be true if the player is an opponent"""
        self.blocked = blocked
        self.number = number
        self.scene = scene
        self.covered_enemies = []
        self.vertices = []
        self.polygon = self.scene.addPolygon(QPolygonF(), QPen(Qt.red))
        self.removePoly()
        self.mittlere_Bewertung = [0,0]

        self.check_box = QCheckBox()
        self.check_box.toggled.connect(self.togglePoly)
        self.check_box.setChecked(True)
        self.check_box.setToolTip("Toggle Polygon display")

        self.scene.positionedSignal.connect(self.savePosition)
        self.scene.resetSignal.connect(self.reset)

        self.ellipse = MyEllipse(self, 0, 0, 20, 20, QPen(Qt.red), QBrush(Qt.red), self.scene)
        self.setLocation(posx, posy)

        with open('config.json') as config_file:
            data = json.load(config_file)
            self.velocity = data['roboter-geschwindigkeit']
            self.change_rotation = data['richtungswechsel-periode']
            self.pos_distance = data['positionierungsdistanz']

        #print("Center:\t" + str(self.ellipse.getCenter())+"\n\t" + str(self.ellipse.x()) + ", " + str(self.ellipse.y()))
        #self.setRotation(-45)


    def setLocation(self, posx, posy):
        """
        :param posx: X-Koordinate des Spielermittelpunkts
        :param posy: Y-Koordinate des Spielermittelpunkts
        """
        self.ellipse.setPos(posx-10, posy-10)

    def getLocation(self):
        """:return: tuple x and y coordinates as integer"""
        return [round(self.ellipse.getX(), 2), round(self.ellipse.getY(), 2)]

    def getLocationArray(self):
        return np.array([[round(self.ellipse.getX(),2), round(self.ellipse.getY(),2)]])

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

    def getPosRaster(self):
        """:returns mögliche Positionen des Angreifers"""
        positions = []

        radius = self.velocity * self.scene.t_move
        # print(type(self))
        # print(self)
        # print("Create distance circle with radius= " + str(radius))
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

    def getRotation(self):
        return self.ellipse.rotation()

    def setRotation(self, rotation):
        self.ellipse.setRotation(rotation)

    def setDirectionColor(self, color: QColor):
        self.ellipse.direction_pen = QPen(color)
        self.ellipse.update()

    def setColor(self, color: QColor):
        self.ellipse.brush = QBrush(color)
        self.ellipse.pen = QPen(color)
        self.ellipse.update()

    def reset(self):
        self.setLocation(self.resetPosition[0], self.resetPosition[1])
        self.setRotation(self.resetRotation)

    def savePosition(self):
        self.resetPosition = self.getLocation()
        self.resetRotation = self.getRotation()

    def __dict__(self):
        return {
            "posx": self.getLocation()[0],
            "posy": self.getLocation()[1]
        }

    def __repr__(self):
        string = ''
        string += str(self.number) + ', '
        string += str(self.ellipse.getX()) + ', '
        string += str(self.ellipse.getY()) + '\n'
        return string

    def __del__(self):
        print("Spieler gelöscht")
        self.scene.removeItem(self.ellipse)
        self.scene.removeItem(self.polygon)


class offensePlayer(Player):
    def __init__(self, number: int, scene: QGraphicsScene, posx=-20, posy=0, blocked=False):
        super().__init__(number, False, scene, posx, posy)

        self.blocked = blocked
        self.scene.addAttacker(self)

        string = "Attacker " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.setColor(Qt.black)
        self.ellipse.setPen(QPen(Qt.black))
        self.ellipse.setToolTip(string)
        self.ellipse.blocked_signal.blockedSignal.connect(self.markAsBlocked)

        self.scene.resetSignal.connect(self.unmarkAsBlocked)

    def unmarkAsBlocked(self):
        self.blocked = False

    def markAsBlocked(self):
        self.blocked = True


class defensePlayer(Player):
    def __init__(self, number: int, scene: QGraphicsScene, posx=20, posy=0, destination=None):
        super().__init__(number, True, scene, posx, posy)

        self.scene.addDefender(self)
        self.scene.resetSignal.connect(self.clearEnemy)
        string = "Defense " + str(self.number)
        self.check_box.setText(string)
        self.check_box.update()

        self.enemy = None
        self.att_distances = {}

        self.enemy_critical_positions = []

        self.setColor(Qt.blue)
        self.ellipse.setToolTip(string)
        self.ellipse.setTransformOriginPoint(10, 10)
        self.ellipse.setRotation(180)
        self.ellipse.update()

    def clearEnemy(self, value=None):
        if value and value == "Strat":
            #print("Gegenspieler vergessen! ")
            self.enemy = None
            self.ellipse.find_enemies = True

    def findEnemy(self, ohne: Player = None):
        """:var enemy Dieser Spieler wird  ausgelassen in der Suche (Für den Fall dass nochmal gesucht werden muss)
            """

        #print("Gegenspieler Suchen! ")

        for x in self.scene.attackers:
            if not x in self.scene.covered_attackers:
                self.enemy = x
                self.scene.covered_attackers.append(x)
                color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.enemy.setDirectionColor(color)
                self.setDirectionColor(color)
                return

        print("------- Kein Gegner gefunden ?! --------")
        print(self.scene.attackers)

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
        """
            * Bewertet die Positionen des Gegners
            * :returns Position an die sich der Spieler bewegen soll
        """
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
            val = evaluatePoint(i[0], i[1])
            point_val.update({str(i):val})

        #Beachte Worstcase:
        max_val = max(point_val.values())
        #print("Worstcase-Positionen:")
        for point, value in point_val.items():
            if value == max_val:
                worst_case_pos_str.append(point)

        for i in worst_case_pos_str:
            #Umwandlung String zu Position
            point = i.strip('][').split(', ')
            point[0] = int(point[0])
            point[1] = int(point[1])
            #print(point)
            worst_case_pos.append(point)
            #self.worstcase_point = self.scene.addEllipse(point[0],point[1],10,10,QPen(Qt.red),QBrush(Qt.red))
        #print(worst_case_pos)
        self.enemy_critical_positions = worst_case_pos

        pos = self.getDefPos()

        return pos

    def getDefPos(self):
        """:returns Array [x,y] wo sich der Spieler positionieren soll"""

        en_current_pos = self.enemy.getLocation()
        dxm = round(self.enemy_critical_positions[0][0] - en_current_pos[0] * self.pos_distance, 2)
        dym = round(self.enemy_critical_positions[0][1] - en_current_pos[1] * self.pos_distance, 2)

        final_pos = [en_current_pos[0]+dxm, en_current_pos[1]+dym]

        return final_pos



