import sys
from MainMenu import MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen



##class Player():
   ## def __init__(self):



##  def paintEvent(self, event):
##      ##Feld zeichnen
##      painter = QtGui.QPainter()
##      color = QtGui.QColor(200, 0, 0)
##      painter.setBrush(color)
##      painter.begin(self)
##      bereich = QtCore.QRect(200, 50, 900, 600)
##      painter.drawRect(bereich)
##      painter.drawEllipse(200, 50, 15, 15)
##      painter.end()


app = QApplication(sys.argv)
w = MainWindow()
w.anzeigen()

sys.exit(app.exec_())
