
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon
from Player import *
from Widgets.InfoBox import InfoBox
from os import listdir
from os.path import isfile, join
from Widgets.MyScene import SoccerScene
from Widgets import MyScene

def buildSmall(self):
    """Layout Erstellung des Frontends, bei kleineren Bildschirmen"""
    horizontallayout = QHBoxLayout()
    verticallayout = QVBoxLayout()

    verticallayout = buildBtns(self, verticallayout)

    horizontallayout.addLayout(verticallayout)

    view = QGraphicsView(self.scene, self)
    view.setGeometry(100, 20, 950, 700)
    view.setMinimumSize(950, 600)

    horizontallayout.addWidget(view)

    verticallayout3 = QVBoxLayout()
    self.textbox = QLineEdit(self)
    self.textbox.resize(100, 20)
    verticallayout3.addWidget(self.textbox)

    self.group_pl, self.group_op = QGroupBox("Offense"), QGroupBox("Defense")
    self.group_pl_layout, self.group_op_layout = QVBoxLayout(), QVBoxLayout()
    self.group_pl.setLayout(self.group_pl_layout)
    self.group_op.setLayout(self.group_op_layout)
    groups_layout = QHBoxLayout()
    groups_layout.addWidget(self.group_pl)
    groups_layout.addWidget(self.group_op)
    verticallayout3.addLayout(groups_layout)

    self.tabWidget = QTabWidget()
    self.info_attackers = InfoBox(self.scene)
    self.info_defenders = InfoBox(self.scene)
    self.tabWidget.addTab(self.info_attackers, "Attackers")
    self.tabWidget.addTab(self.info_defenders, "Defenders")

    verticallayout3.addWidget(self.tabWidget)

    verticallayout3.addStretch(1)

    horizontallayout.addLayout(verticallayout3)

    return horizontallayout

def buildBig(self):
    """Layout Erstellung des Frontends, bei größeren Bildschirmen"""
    horizontallayout = QHBoxLayout()
    verticallayout = QVBoxLayout()

    verticallayout = buildBtns(self, verticallayout)

    horizontallayout.addLayout(verticallayout)

    view = QGraphicsView(self.scene, self)
    view.setGeometry(200, 50, 1000, 700)
    view.setMinimumSize(1000, 700)

    horizontallayout.addWidget(view)

    verticallayout3 = QVBoxLayout()
    self.textbox = QLineEdit(self)
    self.textbox.resize(300, 20)
    self.textbox.setMinimumSize(300, 20)
    verticallayout3.addWidget(self.textbox)

    self.group_pl, self.group_op = QGroupBox("Players"), QGroupBox("Opponents")
    self.group_pl_layout, self.group_op_layout = QVBoxLayout(), QVBoxLayout()
    self.group_pl.setLayout(self.group_pl_layout)
    self.group_op.setLayout(self.group_op_layout)
    groups_layout = QHBoxLayout()
    groups_layout.addWidget(self.group_pl)
    groups_layout.addWidget(self.group_op)
    verticallayout3.addLayout(groups_layout)

    self.tabWidget = QTabWidget()
    self.info_attackers = InfoBox(self.scene)
    self.info_defenders = InfoBox(self.scene)
    self.tabWidget.addTab(self.info_attackers, "Attackers")
    self.tabWidget.addTab(self.info_defenders, "Defenders")

    verticallayout3.addWidget(self.tabWidget)

    verticallayout3.addStretch(1)

    horizontallayout.addLayout(verticallayout3)
    ##self.textbox.setText(str(self.scene.width()) + ", " + str(self.scene.height()))
    ##self.textbox.setText(str(self.player.scenePos()))

    return(horizontallayout)

def buildBtns(self, verticallayout = None):
    """Erstellung der Menü-Buttons"""

    if not verticallayout:
        verticallayout = QVBoxLayout()

    self.general_headline = QLabel('Allgemein:')
    verticallayout.addWidget(self.general_headline)

    self.addplayer = QPushButton('Angreifer')
    self.addplayer.clicked.connect(self.addAttacker)
    verticallayout.addWidget(self.addplayer)

    self.addopponent = QPushButton('Verteidiger')
    self.addopponent.clicked.connect(self.addDefender)
    verticallayout.addWidget(self.addopponent)

    self.posbut = QPushButton("Alle Spieler entfernen")
    self.posbut.clicked.connect(self.click_function)
    verticallayout.addWidget(self.posbut)

    # self.saveButton = QPushButton('save strat')
    # self.saveButton.clicked.connect(self.save_function)
    # verticallayout.addWidget(self.saveButton)
    #
    self.loadButton = QPushButton('Lade Aufstellung')
    self.loadButton.clicked.connect(self.loadFunction)
    verticallayout.addWidget(self.loadButton)

    self.load_final_positions = QPushButton('Lade Endposition')
    self.load_final_positions.clicked.connect(self.loadEndpositions)
    verticallayout.addWidget(self.load_final_positions)

    # self.voronoiButton = QPushButton('Voronoi')
    # self.voronoiButton.clicked.connect(self.vor)
    # verticallayout.addWidget(self.voronoiButton)

    # self.anim = QPushButton('Simple Anim')
    # self.anim.clicked.connect(self.animation)
    # verticallayout.addWidget(self.anim)
    #
    # self.anim = QPushButton('Experiment')
    # self.anim.clicked.connect(self.startExperiment)
    # verticallayout.addWidget(self.anim)


    self.bewertungButton = QPushButton('Bewerten')
    self.bewertungButton.clicked.connect(self.bewerten)
    self.bewertungButton.setEnabled(True)
    verticallayout.addWidget(self.bewertungButton)

    self.analyzeButton = QPushButton('Auswerten')
    self.analyzeButton.clicked.connect(self.analyze)
    self.analyzeButton.setEnabled(True)
    verticallayout.addWidget(self.analyzeButton)
    verticallayout.addStretch(1)

    self.experiment_headline = QLabel('Exeriment:')
    verticallayout.addWidget(self.experiment_headline)

    self.strat_selector1 = QComboBox()
    self.strat_selector1.addItem("Strategie 1")
    self.strat_selector1.currentIndexChanged.connect(self.selectionChange1)

    verticallayout.addWidget(self.strat_selector1)

    self.strat_selector2 = QComboBox()
    self.strat_selector2.addItem("Strategie 2")
    self.strat_selector2.currentIndexChanged.connect(self.selectionChange2)

    verticallayout.addWidget(self.strat_selector2)

    self.compare = QCheckBox('Compare strategies')
    self.compare.toggled.connect(self.toggleCompare)
    verticallayout.addWidget(self.compare)

    self.settest = QPushButton('Strategien Testen')
    self.settest.clicked.connect(self.testSet)
    self.settest.setToolTip('Löscht alle aktuellen Spiler und startet eine Reihe von Tests')
    verticallayout.addWidget(self.settest)

    verticallayout.addStretch(1)
    self.examples_headline = QLabel('Beispiele:')
    verticallayout.addWidget(self.examples_headline)

    self.example_selector_att = QComboBox()
    self.example_selector_att.addItem("Angreifer")
    self.example_selector_att.currentIndexChanged.connect(self.exampleChangeA)

    verticallayout.addWidget(self.example_selector_att)

    self.example_selector_def = QComboBox()
    self.example_selector_def.addItem("Verteidiger")
    self.example_selector_def.currentIndexChanged.connect(self.exampleChangeD)
    verticallayout.addWidget(self.example_selector_def)
    verticallayout.addStretch(1)

    self.restart_button = QPushButton('Restart')
    self.restart_button.clicked.connect(self.restartFunction)
    verticallayout.addWidget(self.restart_button)

    self.closeButton = QPushButton('Exit')
    self.closeButton.clicked.connect(self.close_function)
    verticallayout.addWidget(self.closeButton)

    self.toggleLines = QCheckBox('Priorisierung')
    self.toggleLines.toggled.connect(self.addLines)
    verticallayout.addWidget(self.toggleLines)

    return verticallayout
