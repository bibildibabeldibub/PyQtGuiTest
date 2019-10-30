import math
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon

def counterClockwise(polygon: []):
    poly = QPolygon()
    for p in polygon:
        poly.append(QPoint(p[0], p[1]))
    rect = poly.boundingRect()
    center = rect.center()
    
    return polygon
