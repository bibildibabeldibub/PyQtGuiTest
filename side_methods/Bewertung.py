import math
import Widgets.MyScene
import Player
from PyQt5.QtCore import QPointF, QPoint
from copy import deepcopy
import math
import json


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
    all_scores = evaluateTeam(scene.defenders, remaining_raster)
    # print("Scene Evaluation: ")
    # print(all_scores)
    return all_scores



def evaluateTeam(team, raster):
    scores = {
        "ohne": 0,
        "schussweg": 0,
        "spieler": 0,
        "beides": 0
    }
    remaining_raster = raster

    ohne = 0
    schussweg = 0
    spieler = 0
    beides = 0

    for p in team:
        scoresnew = evaluatePlayer(remaining_raster, p)
        ohne += scoresnew["ohne"]
        schussweg += scoresnew["schussweg"]
        spieler += scoresnew["spieler"]
        beides += scoresnew["beides"]

    scores["ohne"] = ohne
    scores["schussweg"] = schussweg
    scores["spieler"] = spieler
    scores["beides"] = beides

    print(json.dumps(scores, indent=4))

    return scores


def evaluatePlayer(raster, player: Player):
    """
    :param raster: raster of the field with possible areas
    :param defender: player to be scored
    :return: scores of the player
    """

    score = 0
    score_both = 0
    scores = {
        "ohne": 0,
        "schussweg": 0,
        "spieler": 0,
        "beides": 0
    }

    for squaredm in raster:
        if player.polygon.contains(QPointF(squaredm[0], squaredm[1])):
            score += evaluatePoint(squaredm[0], squaredm[1])

    scores["ohne"] = score

    #Angreifer Bonus/Malus ?
    if player.enemy:
        check = checkShootCovered(player)
        if check and check != 0:
            # print("Schussbahn blockiert")
            score_both = score + score/2
            scores["schussweg"] = score + score/2 #->Wert muss noch ausbalanciert werden/getestet max = 1672,43
        elif check == 0:
            # print("Enemy in own half")
            scores["schussweg"] = score
            score_both = score
        else:
            # print("FREIE SCHUSSBAHN!!!!! ")
            scores["schussweg"] = score/2
            score_both = score/2

        if player.enemy.blocked:
            scores["spieler"] = score + 250
            score_both += 250
        else:
            scores["spieler"] = score

        scores["beides"] = score_both
    else:
        print("no enemy")
        for k in scores.keys():
            scores[k] = score
    #print("Count:       " + str(count))

    return scores


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
            # print("Gegner in eigener Hälfte -> Schuss nicht gefährlich")
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
                # print("Schussbahn verdeckt")
                return True
            else:
                return False

    else:
        # print("kein Gegenspieler")
        return False
