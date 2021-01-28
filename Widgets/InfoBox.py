from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Player
from side_methods.Bewertung import evaluatePlayer


class InfoLabel(QLabel):
    def __init__(self, p: Player.Player):
        super().__init__()
        self.update_count = 0
        layout = QVBoxLayout()
        self.p = p

        self.eval = True

        self.l1 = QLabel()
        self.l2 = QLabel()
        self.l3 = QLabel()
        self.l4 = QLabel()

        self.l1.setText("Flächeninhalt:\n  " + str(self.p.area()))
        self.l2.setText("Position:\n  " + str(self.p.getLocation()))
        self.l3.setText(str(self.p))
        self.l4.setText("Punktzahl:\n")

        layout.addWidget(self.l1)
        layout.addWidget(self.l2)
        layout.addWidget(self.l3)
        layout.addWidget(self.l4)

        self.setLayout(layout)

    def updateInfoLabel(self):
        self.l1.setText("Flächeninhalt:\n  " + str(self.p.area()))
        self.l2.setText("Position:\n  " + str(self.p.getLocation()))
        self.l3.setText(str(self.p))
        # if self.eval and self.update_count == 0:
        #     self.l4.setText("Punktzahl:\n " + str(evaluatePlayer(self.parent().parent().scene.unordered_raster, self.p)[1]))
        self.l1.update()
        self.l2.update()
        self.l3.update()
        self.l4.update()
        self.update_count += 1
        if self.update_count >= 30:
            self.update_count = 0

    def toggleEval(self):
        self.eval = not self.eval



class InfoBox(QWidget):
    def __init__(self, scene: QGraphicsScene):
        super(InfoBox, self).__init__()

        self.scene = scene

        horizontallayout = QHBoxLayout()

        self.list_item = QListWidget()
        self.list_item.setMaximumWidth(50)
        self.list_item.currentRowChanged.connect(self.changeInfo)

        self.infos = QStackedWidget()

        horizontallayout.addWidget(self.list_item)
        horizontallayout.addWidget(self.infos)

        self.setLayout(horizontallayout)

    def appendPlayer(self, p: Player.Player):
        self.list_item.insertItem(self.list_item.count(), str(p))
        label = InfoLabel(p)
        self.infos.addWidget(label)

    def changeInfo(self, i):
        #i = self.list_item.currentRow()
        self.infos.setCurrentIndex(i)
        self.infos.widget(i).updateInfoLabel()

    def updateInfo(self):
        for i in range(len(self.infos)):
            self.infos.widget(i).updateInfoLabel()

    def toggleEvaluation(self):
        for i in range(len(self.infos)):
            self.infos.widget(i).toggleEval()

    def removePlayerInfo(self, p):
        for i in range(self.infos.count()):
            widget = self.infos.widget(i)
            print(widget)
            if widget:
                if widget.p == p:
                    self.infos.removeWidget(widget)
            self.list_item.takeItem(i)






