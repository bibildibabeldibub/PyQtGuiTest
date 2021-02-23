
import Player
import random
import json
from datetime import datetime
from side_methods import Bewertung
from side_methods.Logging import JsonLogger

class TestSetUp(object):
    def __init__(self, scene, number=0):
        print("SetUp Creation: " + str(number))
        self.scene = scene
        self.scene.positionedSignal.connect(self.lockSetup)
        self.number = number
        self.angreifer = OffenseTeam(self.scene, 4)
        self.verteidiger = DefenseTeam(self.scene, 4)
        self.score = 0
        self.scores = {}
        self.score_run = 0

        self.lockedAttackers = None
        self.lockedDefenders = None
        self.locked = False

        self.bewerter = Bewertung.Bewerter()
        self.logger = JsonLogger(self, self.scene.date)
        self.writeLog()
        self.changeStrategy()

    def __dict__(self):
        if self.locked:
            return {

                "Attacker": self.lockedAttackers,
                "Defender": self.lockedDefenders,
                "Scores": self.scores
            }
        else:
            return {
                "Attacker": self.angreifer.__dict__(),
                "Defender": self.verteidiger.__dict__(),
                "Scores": self.scores
            }

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def evaluateAll(self):
        run = "run-" + str(self.score_run)
        bewertung = self.bewerter.evaluateScene(self.scene)
        endpositionen = {"Attacker": self.angreifer.__dict__(),
                         "Defender": self.verteidiger.__dict__()}

        bewertung.update(endpositionen)
        self.scores.update({run: bewertung})
        self.score_run += 1

    def writeLog(self):
        self.logger.writeText(json.dumps(self.__dict__(), indent=4))

    def lockSetup(self):
        self.lockedAttackers = self.angreifer.__dict__()
        self.lockedDefenders = self.verteidiger.__dict__()
        self.locked = True

    def changeStrategy(self):
        """Ändert das Logfile der Aufstellung
        * Setzt Zähler zurück, damit die Daten korrekt geloggt werden.
        """

        strat = self.scene.getCurrentStrat()
        file = strat.split(".")
        file = file[0]
        self.logger.setFile(file)
        self.scores = {}
        self.score_run = 0

    def stopBewerter(self):
        del self.bewerter

    def __del__(self):
        print("SetUp Deletion: " + str(self.number))


class Team(object):
    def __init__(self):
        self.spieler = {}

    def __dict__(self):
        player_position_dictionary = {}

        for k in self.spieler.keys():
            o = self.spieler[k].__dict__()
            player_position_dictionary.update({k: o})

        return player_position_dictionary

    def __del__(self):
        self.spieler.clear()


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

