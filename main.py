import sys
from MainMenu import MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen

if __name__ == "__main__":
    exit_code = -666
    while exit_code == -666:
        app = QApplication(sys.argv)
        w = MainWindow()
        w.anzeigen()
        exit_code = app.exec_()
        del app
        del w

    sys.exit(exit_code)

