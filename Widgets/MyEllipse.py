from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QPen, QPolygonF
from PyQt5.QtCore import Qt, QLineF, QPointF, QObject, pyqtSignal, pyqtSlot
import warnings
import numpy as np


class ItemMoveSignal(QObject):
    positionMove = pyqtSignal()


class MyEllipse(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, pen, brush, scene: QGraphicsScene):
        super().__init__(x, y, w, h)

        scene.addItem(self)
        self.s = ItemMoveSignal()
        self.scene = scene
        self.setPen(pen)
        self.setBrush(brush)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.s.positionMove.emit()

        return super().itemChange(change, value)

