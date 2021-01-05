import math
import Widgets.MyScene
import Player
from PyQt5.QtCore import QPointF
from copy import deepcopy

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

# def evaluateDefense(players: list[player]):
#     """
#
#     :param players: players to evaluate
#     :return score: value of the players
#     """
#
#     score = 0
#     for p in players:
#         score += evaluatePlayer(p)
#
#     return score


def evaluatePlayer(raster, defender: Player):
    """

    :param raster: raster of the field with possible areas
    :param defender: player to be scored
    :return: remaining raster and score of the player
    """
    score = 0
    count = 0
    raster_2 = deepcopy(raster)
    for squaredm in raster:
        if defender.polygon.contains(QPointF(squaredm[0], squaredm[1])):
            #print(squaredm)
            score += evaluatePoint(squaredm[0], squaredm[1])
            raster_2.remove(squaredm)
            count += 1

    #print("Count:       " + str(count))
    return [raster_2, score]
