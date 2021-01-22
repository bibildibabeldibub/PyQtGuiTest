
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon
from Player import *
from Widgets.InfoBox import InfoBox
from os import listdir
from os.path import isfile, join
from Widgets.MyScene import SoccerScene
from Widgets import MyScene

def buildSmall(self):
    horizontallayout = QHBoxLayout()
    verticallayout = QVBoxLayout()

    self.start_selector = QComboBox()
    self.start_selector.addItem("Auswählen")
    self.start_selector.currentIndexChanged.connect(self.selectionchange)

    verticallayout.addWidget(self.start_selector)

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
    self.infoAttackers = InfoBox(self.scene)
    self.infoDefenders = InfoBox(self.scene)
    self.tabWidget.addTab(self.infoAttackers, "Attackers")
    self.tabWidget.addTab(self.infoDefenders, "Defenders")

    verticallayout3.addWidget(self.tabWidget)

    verticallayout3.addStretch(1)

    horizontallayout.addLayout(verticallayout3)

    return horizontallayout

def buildBig(self):
    """Creating the main window, with several buttons and the field simulator for huge screens """
    horizontallayout = QHBoxLayout()
    verticallayout = QVBoxLayout()

    """Setup ComboBox"""
    self.start_selector = QComboBox()
    self.start_selector.addItem("Auswählen")
    self.start_selector.currentIndexChanged.connect(self.selectionchange)

    verticallayout.addWidget(self.start_selector)

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
    self.infoAttackers = InfoBox(self.scene)
    self.infoDefenders = InfoBox(self.scene)
    self.tabWidget.addTab(self.infoAttackers, "Attackers")
    self.tabWidget.addTab(self.infoDefenders, "Defenders")

    verticallayout3.addWidget(self.tabWidget)

    verticallayout3.addStretch(1)

    horizontallayout.addLayout(verticallayout3)
    ##self.textbox.setText(str(self.scene.width()) + ", " + str(self.scene.height()))
    ##self.textbox.setText(str(self.player.scenePos()))

    return(horizontallayout)

def buildBtns(self, verticallayout = None):

    if not verticallayout:
        verticallayout = QVBoxLayout

    self.addplayer = QPushButton('add offense')
    self.addplayer.clicked.connect(self.addAttacker)
    verticallayout.addWidget(self.addplayer)

    self.addopponent = QPushButton('add defense')
    self.addopponent.clicked.connect(self.addDefender)
    verticallayout.addWidget(self.addopponent)

    self.posbut = QPushButton("remove all players")
    self.posbut.clicked.connect(self.click_function)
    verticallayout.addWidget(self.posbut)

    self.saveButton = QPushButton('save strat')
    self.saveButton.clicked.connect(self.save_function)
    verticallayout.addWidget(self.saveButton)

    self.loadButton = QPushButton('load strat')
    self.loadButton.clicked.connect(self.load_function)
    verticallayout.addWidget(self.loadButton)

    self.voronoiButton = QPushButton('Voronoi')
    self.voronoiButton.clicked.connect(self.vor)
    verticallayout.addWidget(self.voronoiButton)

    self.anim = QPushButton('Simple Anim')
    self.anim.clicked.connect(self.animation)
    verticallayout.addWidget(self.anim)

    self.anim = QPushButton('Experiment')
    self.anim.clicked.connect(self.startExperiment)
    verticallayout.addWidget(self.anim)

    self.settest = QPushButton('Test Set')
    self.settest.clicked.connect(self.testSet)
    verticallayout.addWidget(self.settest)

    self.resetButton = QPushButton('reset')
    self.resetButton.clicked.connect(self.reset)
    self.resetButton.setEnabled(False)
    verticallayout.addWidget(self.resetButton)

    verticallayout.addStretch(1)

    self.closeButton = QPushButton('Exit')
    self.closeButton.clicked.connect(self.close_function)
    verticallayout.addWidget(self.closeButton)

    self.toggleLines = QCheckBox('Linien')
    self.toggleLines.toggled.connect(self.add_lines)
    verticallayout.addWidget(self.toggleLines)

    return verticallayout
