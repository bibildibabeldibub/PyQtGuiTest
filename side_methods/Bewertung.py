import math
import Widgets.MyScene
import Player
from PyQt5.QtCore import QPointF, QPoint
from copy import deepcopy
import math
import json


class Bewerter(object):
    def __init__(self):
        super().__init__()
        self.team = None
        self.scene = None
        self.remaining_raster = None

    def evaluatePoint(self, x: float, y: float):
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

    def evaluateScene(self, scene: Widgets.MyScene.SoccerScene):
        self.remaining_raster = scene.unordered_raster
        self.scene = scene
        score_ohne = self.evaluateDefense(scene.defenders, self.remaining_raster)

        print(score_ohne)

        all_scores = self.evaluateOffense(score_ohne)

        print(json.dumps(all_scores, indent=4))

        return all_scores

    def evaluateOffense(self, score):

        schussweg = score
        score_blocked = score
        score_both = score

        for p in self.scene.attackers:
            check = self.checkShootCovered(p)
            if check and check != -1:
                print("Schussbahn blockiert -> kein Malus")
            elif check == -1:
                print("Enemy in eigener Hälfte -> kein Malus")
            else:
                print("FREIE SCHUSSBAHN!!!!! ")
                schussweg -= score/8       #-> maximal -50%
                score_both -= score/8

            if p.blocked:
                score_blocked += score/16 #-> maximal +25%
                score_both += score/16

        scores = {
            "ohne": round(score, 2),
            "schussweg": round(schussweg, 2),
            "spieler": round(score_blocked, 2),
            "beides": round(score_both, 2)
        }

        return scores

    def evaluateDefense(self, team, raster):

        remaining_raster = raster
        score = 0
        for p in team:
            scorenew = self.evaluatePlayer(remaining_raster, p)
            score += scorenew

        return score


    def evaluatePlayer(self, raster, player: Player):
        """
        :param raster: raster of the field with possible areas
        :param defender: player to be scored
        :return: scores of the player
        """
        score = 0

        for squaredm in raster:
            if player.polygon.contains(QPointF(squaredm[0], squaredm[1])):
                score += self.evaluatePoint(squaredm[0], squaredm[1])

        return score


    def checkShootCovered(self, o: Player):
        """
        Überprüft den Schussweg des Angreifers
        :param o: Angreifer
        :return: True wenn der Schussweg blockiert ist, andernfalls nicht

        """

        #erstmal zum mittelpunkt des Tores (450, 0) ODER gerade Schüsse in Rotationsrichtung
        y_oberer_pfosten = -75
        y_unterer_pfosten = 75

        p1 = o.getLocation()
        x_attacker = p1[0]
        y_attacker = p1[1]

        if x_attacker <= 0:
            """check ob nah genug an Tor für gefährlichen Schuss -> Halbes Spielfeld"""
            # print("Gegner in eigener Hälfte -> Schuss nicht gefährlich")
            return -1

        schatten = []

        for d in self.scene.defenders:
            print(d)
            x_defender = d.getLocation()[0]
            y_defender = d.getLocation()[1]
            y_oberer_bauch = y_defender - 10
            y_unterer_bauch = y_defender + 10

            if x_attacker >= x_defender:
                'Angreifer ist auf gleicher oder näher am Tor als Verteidiger'
                continue

            y_oberer_schatten = (y_oberer_bauch - y_attacker) * (450 - x_attacker) / (x_defender - x_attacker) + y_attacker
            y_unterer_schatten = (y_unterer_bauch - y_attacker) * (450 - x_attacker) / (x_defender - x_attacker) + y_attacker

            if y_oberer_schatten <= y_oberer_pfosten:
                if y_unterer_schatten < y_oberer_pfosten:
                    # print("Schatten über Tor")
                    continue
                elif y_unterer_schatten >= y_unterer_pfosten:
                    # print("Schatten verdeckt das komplette Tor")
                    return True
                else:
                    """Schatten schneidet oberen Pfosten"""
                    tor_schatten_oben = y_oberer_pfosten
                    tor_schatten_unten = y_unterer_schatten
            elif y_oberer_pfosten < y_oberer_schatten < y_unterer_pfosten:
                if y_unterer_schatten < y_unterer_pfosten:
                    """Beide Schattengrenzen innerhalb des Tores"""
                    tor_schatten_oben = y_oberer_schatten
                    tor_schatten_unten = y_unterer_schatten
                else:
                    """Schatten überschneidet unteren Pfosten"""
                    tor_schatten_oben = y_oberer_schatten
                    tor_schatten_unten = y_unterer_pfosten
            else:
                """Schatten liegt unter dem Tor"""
                continue

            print([tor_schatten_oben, tor_schatten_unten])

            if len(schatten) == 0:
                schatten.append([tor_schatten_oben, tor_schatten_unten])

            else:
                pos = 0
                pos_dif = None
                for s in schatten:
                    if tor_schatten_oben < s[0]:
                        """Oberkante befindet sich über alter Kante"""
                        if tor_schatten_unten < s[0]:
                            """neuer Schatten komplett über bestehendem"""
                            schatten.insert(pos, [tor_schatten_oben, tor_schatten_unten])
                            break
                        elif s[0] <= tor_schatten_unten <= s[1]:
                            """neuer Schatten schneidet bestehendem -> Aktualisierung Oberkante"""
                            s[0] = tor_schatten_oben
                            break
                        elif s[1] <= tor_schatten_unten:
                            """neuer Schatten überlagert bestehenden"""
                            unterkanten_wert, pos_dif = self.checkNext(tor_schatten_unten, schatten, pos+1)
                            s[0] = tor_schatten_oben
                            s[1] = unterkanten_wert
                            break

                    elif s[0] <= tor_schatten_oben <= s[1]:
                        """Oberkante des neuen Schattens befindet sich in bestehendem Schatten"""
                        if s[1] < tor_schatten_unten:
                            """ersetzen der unteren Schattenkante"""
                            unterkanten_wert, pos_dif = self.checkNext(tor_schatten_unten, schatten, pos+1)
                            s[1] = unterkanten_wert
                            break
                        else:
                            """Schatten wird bereits verdeckt"""
                            break
                    elif pos == len(schatten)-1:
                        schatten.append([tor_schatten_oben, tor_schatten_unten])
                        break

                    pos += 1

                if pos_dif and pos+1 < len(schatten):
                    print(pos_dif)
                    print(pos)
                    for p in range(pos, pos_dif):
                        """Entfernen überschatteter Schattenelemente
                        pos ist das bearbeite Element 
                        pos_dif ist das letzte überschattete Element"""
                        schatten.pop(pos+1)

        print("Finaler Schattenwurf: " + str(schatten))
        verdeckt = 0
        for s in schatten:
            verdeckt += s[1]-s[0]

        if verdeckt >= 0.5*(y_unterer_pfosten-y_oberer_pfosten):
            print("Schussbahn verdeckt")
            return True
        else:
            print("Schussbahn frei")
            return False

    def checkNext(self, unterkante, all_schatten, pos):
        """
        :param unterkante: Unterkantenwert der überprüft wird
        :param all_schatten: Liste aller Elemente
        :param pos: zu untersuchende Position
        :return: neue Unterkante & Position des letzten betroffenen Elements
        """
        if pos < len(all_schatten):
            if unterkante < all_schatten[pos][0]:
                """Unterkante reicht nicht bis in den nächsten Schatten"""
                return unterkante, pos-1
            elif unterkante < all_schatten[pos][1]:
                """Unterkante reicht bis in diesen Schatten"""
                return all_schatten[pos][1], pos
            else:
                """Unterkante könnte in nächsten Schatten reichen"""
                return self.checkNext(unterkante, all_schatten, pos+1)
        else:
            """Unterkante letzte untere Kante"""
            return unterkante, pos


