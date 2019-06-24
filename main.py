import sys
from MainMenu import MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen


app = QApplication(sys.argv)
w = MainWindow()
w.anzeigen()

sys.exit(app.exec_())
