
import Player
import random
import json
from side_methods import Bewertung
from side_methods.Logging import JsonLogger

class TestSetUp(object):
    def __init__(self, scene):
        self.scene = scene
        self.angreifer = OffenseTeam(self.scene, 4)
        self.verteidiger = DefenseTeam(self.scene, 4)
        self.score = 0
        self.scores = {}
        self.Logger = JsonLogger()
        self.score_run = 0

    def __dict__(self):
        return {
            "Angreifer": self.angreifer.__dict__(),
            "Verteidiger": self.verteidiger.__dict__(),
            "Scores": self.scores
        }

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def evaluateAll(self):
        run = "run-" + str(self.score_run)
        self.scores.update({run: Bewertung.evaluateScene(self.scene)})
        self.score_run += 1

    def writeLog(self):
        self.Logger.writeText(json.dumps(self))


class Team(object):
    def __init__(self):
        self.spieler = {}

    def __dict__(self):
        player_position_dictionary = {}

        for k in self.spieler.keys():
            o = self.spieler[k].__dict__()
            print(o)
            player_position_dictionary.update({k: o})

        print(player_position_dictionary)

        return player_position_dictionary


class OffenseTeam(Team):
    def __init__(self, scene, length):
        super().__init__()
        self.scene = scene
        self.length = length
        for i in range(self.length):
            p = Player.offensePlayer(i, self.scene, posx=random.uniform(-450, 0), posy=random.uniform(-300, 300))
            self.spieler.update({i: p})

class DefenseTeam(Team):
    def __init__(self, scene, length):
        super().__init__()
        self.scene = scene
        self.length = length
        x_count = 1
        for i in range(self.length):
            if i % 2 == 0:
                self.spieler.update({i: Player.defensePlayer(i, self.scene, posx=50 * x_count, posy=-300)})
            else:
                self.spieler.update({i: Player.defensePlayer(i, self.scene, posx=x_count * 50, posy=300)})
            x_count += 1

