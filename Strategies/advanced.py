import math
import time
import Widgets
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

    angreifer = scene.attackers
    max_x_ang = -450
    index = 0
    for a in angreifer:
        if a.getLocation()[0] > max_x_ang:
            max_x_ang = a.getLocation()[0]
            index = angreifer.index(a)

    aggr = angreifer[index]

    if 0 <= defender.new_pos[0] <= 50:
        '''Verteidiger an der Mittellinie'''
        defender.new_pos[0] = defender.new_pos[0] + max_x_ang+250
        # if defender.enemy.getLocation()[0] <= -225:
        #     dummy = QGraphicsRectItem(0, -300, 50, 600)
        #     collision = scene.items(dummy.shape())
        #     collision = [o for o in collision if type(o) == Widgets.MyEllipse.MyEllipse and o is not defender.ellipse]
        #     if collision:
        #         for e in collision:
        #             v = e.spieler




    '''Verteidiger am Spielfeldrand'''
    if defender.getLocation != defender.new_pos:
        print("Verteidiger am Spielfeldrand ! --------")
        dummy = QGraphicsEllipseItem(aggr.getLocation()[0]+300-100, 0.9 * aggr.getLocation()[1], 20, 20)
        collision = scene.items(dummy.shape())
        collision = [o for o in collision if o is not defender.ellipse and type(o) == Widgets.MyEllipse.MyEllipse]
        if not collision:
            defender.new_pos = [aggr.getLocation()[0]+300, aggr.getLocation()[1]]
        else:
            defender.new_pos = [0, aggr.getLocation()[1]]

    '''Verteidiger die eng zusammenstehen'''
    dummy_ellipse = QGraphicsEllipseItem(defender.getLocation()[0]-22.5, defender.getLocation()[1]-22.5, 45, 45)
    collision = scene.items(dummy_ellipse.shape())
    collision = [o for o in collision if o is not defender.ellipse and type(o) is Widgets.MyEllipse.MyEllipse]
    if collision:
        print("Verteidiger Cluster  ! --------")
        '''Nur der vorderste Spieler bleibt an Position'''
        cluster = [defender]
        cluster_max_x = defender.new_pos[0]
        for e in collision:
            cluster.append(e.spieler)
            if e.spieler.getLocation()[0] > cluster_max_x:
                cluster_max_x = e.spieler.getLocation()[0]
        if defender.new_pos[0] != cluster_max_x:
            defender.new_pos[0] = defender.new_pos[0]+100



    defender.setLocation(defender.new_pos[0], defender.new_pos[1])
    return
