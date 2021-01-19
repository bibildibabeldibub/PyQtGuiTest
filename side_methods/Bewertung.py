import math
import Widgets.MyScene
import Player
from PyQt5.QtCore import QPointF, QPoint
from copy import deepcopy
import math

def evaluatePoint(x: float, y: float):
        """:returns Wert an dem Punkt"""
        # print("\n--------------------")
        # print("Mittelpunkt: " + str(x) + "|" + str(y) )
        dx = 450 - x
        dy = 0 - y
        distance = math.sqrt(dx*dx+dy*dy)
        wert = 100/distance
        # print("Distanz:" + str(distance))
        # print("Wert:" + str(wert))
        return wert

def evaluateScene(scene: Widgets.MyScene.SoccerScene):
    remaining_raster = scene.unordered_raster
    resd = evaluateTeam(scene.defenders, remaining_raster)
    remaining_raster = resd[0]
    score_def = resd[1]

    resa = evaluateTeam(scene.attackers, remaining_raster)
    remaining_raster = resa[0]
    score_att = resa[1]

    text = "\nAngreifer Punktzahl:       " + str(score_att)
    text += "\nVerteidiger Punktzahl:     " + str(score_def)
    return text



def evaluateTeam(team, raster):
    score = 0
    for p in team:
        res = evaluatePlayer(raster, p)
        raster = res[0]
        score += res[1]
        #print(str(p) + ":       " + str(res[1]))
    #print("Gesamt: \t" + str(score))

    return [raster, score]


def evaluatePlayer(raster, player: Player):
    """

    :param raster: raster of the field with possible areas
    :param defender: player to be scored
    :return: remaining raster and score of the player
    """
    score = 0
    count = 0
    raster_2 = deepcopy(raster)
    for squaredm in raster:
        if player.polygon.contains(QPointF(squaredm[0], squaredm[1])):
            #print(squaredm)
            score += evaluatePoint(squaredm[0], squaredm[1])
            raster_2.remove(squaredm)
            count += 1

    #Angreifer Bonus/Malus ?
    if type(player) == Player.defensePlayer:
        if player.enemy:
            check = checkShootCovered(player)
            if check:
                if check == 0:
                    score += 0
                print("Schussbahn blockiert")
                score += 500                    #->Wert muss noch ausbalanciert werden/getestet max = 1672,43 
            else:
                print("FREIE SCHUSSBAHN!!!!! ")

            if player.enemy.blocked:
                score += 250
        else:
            print("no enemy")
    #print("Count:       " + str(count))




    return [raster_2, score]


def checkShootCovered(d: Player):
    """
    Überprüft den Schussweg des Gegenspielers
    :param d: Verteiger
    :return: True wenn der Schussweg blockiert ist, andernfalls nicht

    """
    #erstmal zum mittelpunkt des Tores (450, 0) ODER gerade Schüsse in Rotationsrichtung
    y_oberer_pfosten = -75
    y_unterer_pfosten = 75
    o = d.enemy
    if o:
        p1 = o.getLocation()

        if p1[0] <= 0:
            print("Gegner in eigener Hälfte -> Schuss nicht gefährlich")
            return 0

        if p1[0] > 0:
            """check ob nah genug an Tor für gefährlichen Schuss -> Halbes Spielfeld"""

            y_defender = d.getLocation()[1]
            y_oberer_bauch = y_defender - 10
            y_unterer_bauch = y_defender + 10

            winkel_ober_pfosten = math.degrees(math.atan(y_oberer_pfosten - p1[1]/450-p1[0]))
            winkel_unter_pfosten = math.degrees(math.atan(y_unterer_pfosten - p1[1]/450-p1[0]))
            schusswinkel = abs(winkel_unter_pfosten) + abs(winkel_ober_pfosten)

            winkel_ober_bauch = math.degrees(math.atan(y_oberer_bauch - p1[1] / 450 - p1[0]))
            winkel_unter_bauch = math.degrees(math.atan(y_unterer_bauch - p1[1] / 450 - p1[0]))

            if winkel_ober_bauch <= winkel_ober_pfosten and winkel_unter_bauch >= winkel_unter_pfosten:
                """100% Verdeckt"""
                return True

            elif winkel_ober_bauch > winkel_ober_pfosten and winkel_unter_bauch < winkel_unter_pfosten:
                """Verteidiger befindet sich komplett im Schusskegel"""
                verdeckt = abs(winkel_ober_bauch) + abs(winkel_unter_bauch)

            elif winkel_ober_bauch <= winkel_ober_pfosten and winkel_unter_bauch > winkel_ober_pfosten:
                """Verdeckt den oberen Pfosten"""
                verdeckt = winkel_ober_pfosten - winkel_unter_bauch

            elif winkel_ober_bauch < winkel_unter_pfosten and winkel_unter_bauch >= winkel_unter_pfosten:
                verdeckt = winkel_unter_pfosten - winkel_ober_bauch

            else:
                return False

            if verdeckt >= 0.5*schusswinkel:
                print("Schussbahn verdeckt")
                return True
            else:
                return False

    else:
        print("kein Gegenspieler")
        return False
