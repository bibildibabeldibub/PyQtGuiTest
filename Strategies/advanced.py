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
    naiv_pos = [round(naiv_pos[0], 2),round(naiv_pos[1], 2)]
    defender.new_pos = naiv_pos

    return naiv_pos

def advanced(defender :Player, attacker, scene):
    """Erfassung von Redundanten Spielern"""
    if scene.phase == 1:
        return
    print("Advanced Positioning! ")
    if defender.repositioned:
        return
    defender.new_pos[0] = round(defender.new_pos[0], 2)
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
        if max_x_ang > -75:
            if defender.enemy.getLocation()[0] < -230:
                dummy = QGraphicsRectItem(0, -300, 20, 600)
                collision = scene.items(dummy.shape())
                collision = [o for o in collision if o is not defender.ellipse and type(o) == Widgets.MyEllipse.MyEllipse]
                if 2 <= len(collision):
                    ypsilons = []
                    distances = []
                    for e in collision:   # e = Ellipse
                        ypsilons.append(e.spieler.getLocation()[1])
                        v = [defender.getLocation()[0]-e.spieler.getLocation()[0], defender.getLocation()[1]-e.spieler.getLocation()[1]]
                        distances.append(betrag(v))
                    if min(ypsilons) < defender.getLocation()[1] < max(ypsilons) and min(distances) < 150:
                        '''Verschieben zu Aggressor unter gegebenen Voraussetzungen'''
                        defender.new_pos[1] = aggr.getLocation()[1]
                        defender.new_pos[0] = aggr.getLocation()[0] + 45
            else:
                defender.new_pos[0] = max_x_ang + 125

    elif defender.getLocation()[1] == 300 or defender.getLocation()[1] == -300:
        '''Verteidiger am Spielfeldrand'''
        print("Verteidiger am Spielfeldrand ! --------")
        dummy = QGraphicsEllipseItem(aggr.getLocation()[0]+300 - 22.5, 0.9 * aggr.getLocation()[1] - 22.5, 45, 45)
        collision = scene.items(dummy.shape())
        collision = [o for o in collision if o is not defender.ellipse and type(o) == Widgets.MyEllipse.MyEllipse]
        if not collision:
            defender.new_pos = [aggr.getLocation()[0]+300, aggr.getLocation()[1]]
        else:
            defender.new_pos = [0, aggr.getLocation()[1]]
            defender.repositioned = True

    '''Verteidiger die eng zusammenstehen'''
    dummy_ellipse = QGraphicsEllipseItem(defender.getLocation()[0]-22.5, defender.getLocation()[1]-22.5, 45, 45)
    dummy_ellipse.setPen(QPen(Qt.black))
    scene.addItem(dummy_ellipse)
    collision = scene.items(dummy_ellipse.shape())
    scene.removeItem(dummy_ellipse)
    collision = [o for o in collision if o is not defender.ellipse and type(o) is Widgets.MyEllipse.MyEllipse]
    collision = [o for o in collision if type(o.spieler) == Player.defensePlayer]
    if collision:
        print("Verteidiger Cluster  ! --------")
        cluster = [defender]
        cluster_min_x = defender.new_pos[0]
        for e in collision:
            cluster.append(e.spieler)
            if e.spieler.getLocation()[0] < cluster_min_x:
                cluster_min_x = e.spieler.getLocation()[0]
        # if defender.new_pos[0] != cluster_min_x:
        #     '''Nur der vorderste Spieler bleibt an Position'''
            # defender.new_pos[0] = defender.new_pos[0]+50
        mitte_x = 0
        mitte_y = 0

        for p in cluster:
            mitte_x += p.getLocation()[0]
            mitte_y += p.getLocation()[1]
        mitte_x = mitte_x/len(cluster)
        mitte_y = mitte_y/len(cluster)
        #scene.addEllipse(mitte_x-5, mitte_y-5, 10, 10, QPen(Qt.darkGreen), QBrush(Qt.darkGreen))
        v = [defender.new_pos[0] - mitte_x, defender.new_pos[1] - mitte_y]
        n = 50/betrag(v)
        z = [v[0]*n, v[1]*n]
        defender.new_pos[0] = mitte_x + z[0]
        defender.new_pos[1] = mitte_y + z[1]
        defender.repositioned = True
    defender.setLocation(defender.new_pos[0], defender.new_pos[1])
    return
