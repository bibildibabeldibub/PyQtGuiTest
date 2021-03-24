import math
import time

import Player
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

def betrag(vec: list):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def strat(defender, attacker, scene):
    """
    @param attacker: zugeordneter Angreifer
    @param scene: Spielszene
    @return: Position to move
    """
    attacker_pos = attacker.getLocation()
    goal_pos = [450, 0]
    vec = [goal_pos[0] - attacker_pos[0], goal_pos[1] - attacker_pos[1]]
    n = 250 / betrag(vec)
    naiv_pos = [attacker_pos[0] + vec[0]*n, attacker_pos[1] + vec[1]*n]
    if naiv_pos[0] < 0:
        '''Verschieben in eigene Hälfte'''
        m = attacker_pos[0] / (goal_pos[0] - attacker_pos[0])
        y_d = vec[1] * m
        naiv_pos = [attacker_pos[0] - attacker_pos[0], attacker_pos[1] - y_d]

    defender.new_pos = naiv_pos

    return naiv_pos

def advanced(defender :Player, attacker, scene):
    """Erfassung von Redundanten Spielern"""

    print("Advanced Positioning! ")
    defender.setLocation(defender.new_pos[0], defender.new_pos[1])
    # defender_list = scene.defenders
    # defender_coords = []
    # for d in defender_list:
    #     defender_coords.append(d.new_pos)
    # print(defender_coords)
    #
    # center_x = 0
    # center_y = 0
    # for p in defender_coords:
    #     center_x += p[0]
    #     center_y += p[1]
    #
    # scene.addEllipse(center_x/len(defender_coords), center_y/len(defender_coords), 10, 10, brush=QBrush(Qt.darkGray), pen=QPen(Qt.green))
    #
    # scene.addEllipse(center_x, center_y, 10, 10, brush=QBrush(Qt.red), pen=QPen(Qt.green))
    #
    # print("Center:\t{x}|{y}".format(x=center_x, y=center_y))
    dummy_ellipse = QGraphicsEllipseItem(defender.new_pos[0] - 45, defender.new_pos[1] - 45, 90, 90)
    colliding_items = scene.items(dummy_ellipse.shape())
    scene.addItem(dummy_ellipse)
    time.sleep(1)
    scene.removeItem(dummy_ellipse)
    mates_around = [o for o in colliding_items if (type(o) == Player.defensePlayer) and (o is not defender.ellipse)]

    if mates_around:
        '''Anderer Verteidiger steht auf der Position oder ist zu nah'''
        print("Density to high")
        center_x = defender.new_pos[0]
        center_y = defender.new_pos[1]
        for mate_ellipse in mates_around:
            center_x += mate_ellipse.s.new_pos[0]
            center_y += mate_ellipse.s.new_pos[1]
        center_x = center_x/(len(mates_around)+1)
        center_y = center_y/(len(mates_around)+1)
        center_test = scene.addEllipse(center_x, center_y, 10, 10, brush=QBrush(Qt.red), pen=QPen(Qt.green))
        time.sleep(1)
        scene.removeItem(center_test)



    return "test!"
