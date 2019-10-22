from checkPointOnLine import checkPointOnLine
from copy import deepcopy

def splitPolygon(schnittpunkte, polygon):
    """returns 2 polygons splitted bei intersection points with the outer polygon, returns None if both points are on the same line"""
    eckidx = 0
    firstPoly = []
    indices = []
    copy = deepcopy(polygon)
    for eck in polygon:                                 ## test auf welcher Linie die Schnittpunkte liegen
        if eckidx < len(polygon) - 1:
            l = [eck, polygon[eckidx + 1]]
        else:
            l = [eck, polygon[0]]
        for s in schnittpunkte:
            check = checkPointOnLine(s, l)
            if check:
                copy.insert(copy.index(eck) + 1, s)  # einfügen der schnittpunkte in field_copy
                indices.append(copy.index(eck) + 1)
        eckidx += 1

    # aufteilen der polygone
    if indices[0] == indices[1]:
        val = None
    else:
        popcounter = 0
        for i in range(indices[0], indices[1] + 1):
            if i > indices[0] and i < indices[1]:
                firstPoly.append(copy.pop(i-popcounter))
                popcounter += 1
            else:
                firstPoly.append(copy[i-popcounter])
        val = firstPoly, copy

    return val
