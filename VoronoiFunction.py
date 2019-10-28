from scipy.spatial import Voronoi
from PyQt5.QtCore import QPointF, QPoint, Qt
from PyQt5.QtGui import QPolygonF, QPolygon
import numpy as np
import pyclipper
from copy import deepcopy
from side_methods.LinesToPolygon import lines_to_polygon as ltp
from side_methods.polygonSplitter import splitPolygon
from side_methods.checkPointOnLine import checkPointOnLine


def voronoi_function(list_players, list_opponents, field):
    points = []
    for o in list_opponents:
        points.append(o.getLocation())
    for p in list_players:
        points.append(p.getLocation())


    if len(list_players + list_opponents) == 1:
        field = [QPoint(field[0][0], field[0][1]), QPoint(field[1][0], field[1][1]),
                 QPoint(field[2][0], field[2][1]), QPoint(field[3][0], field[3][1])]
        if list_players:
            list_players[0].polygon.setPolygon(QPolygonF(QPolygon(field)))
            return
        if list_opponents:
            list_opponents[0].polygon.setPolygon(QPolygonF(QPolygon(field)))
            return

    if len(points) == 2:
        startpoints = np.array(points)
        print(startpoints)
        mitte = startpoints.mean(axis=0)
        print(mitte)
        #mitte = [(points[0][0]+points[1][0])/2, (points[0][1]+points[1][1])/2]
        v = startpoints[0] - startpoints[1]
        print(v)
        n = np.linalg.norm(v)                            #orthogonaler vektor
        p1 = mitte + 50000 * n
        p2 = mitte + (-50000) * n
        pc = pyclipper.Pyclipper()
        pc.AddPath(field, pyclipper.PT_CLIP, True)
        pc.AddPath([p1, p2], pyclipper.PT_SUBJECT, False)
        line = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        line = pyclipper.PolyTreeToPaths(line)
        print(line[0])
        firstPoly, secondPoly = splitPolygon(line[0], field)
        firstpol = QPolygon()
        secondpol = QPolygon()

        for p in firstPoly:
            firstpol.append(QPoint(p[0], p[1]))
        for p in secondPoly:
            secondpol.append(QPoint(p[0], p[1]))

        for p in list_opponents + list_players:
            if firstpol.containsPoint(QPoint(p.getLocation()[0], p.getLocation()[1]), Qt.OddEvenFill):
                p.polygon.setPolygon(QPolygonF(firstpol))
            if secondpol.containsPoint(QPoint(p.getLocation()[0], p.getLocation()[1]), Qt.OddEvenFill):
                p.polygon.setPolygon(QPolygonF(secondpol))
        return

    pointArray = np.asarray(points)
    vor = Voronoi(pointArray)
    vertices = vor.ridge_vertices
    eckpunkte = vor.vertices
    print("Points: " + str(vor.points))
    print("Ridge_Vertices: " + str(vertices))
    print("Vertices: " + str(eckpunkte.tolist()))
    print("Ridge_Points: " + str(vor.ridge_points))
    print("Regions: " + str(vor.regions))
    print("Point_regions" + str(vor.point_region))


    pointidx = 0
    val = []
    for point in vor.points:  ##iteration über punkte
        lines = []
        schnittpunkte = []
        far_line = []
        regions = vor.regions
        regionidx = vor.point_region.tolist()[pointidx]
        print("\n\n")
        print(pointidx)
        print(vor.points[pointidx])
        print(regions[regionidx])
        if min(regions[regionidx], default=-1) >= 0:        ##behandlung falls polygon geschlossen
            poly = []
            for vidx in regions[regionidx]:
                poly.append([vor.vertices[vidx][0], vor.vertices[vidx][1]])

            pc = pyclipper.Pyclipper()
            pc.AddPath(field, pyclipper.PT_CLIP, True)
            pc.AddPath(poly, pyclipper.PT_SUBJECT, True)
            poly = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            poly = pyclipper.PolyTreeToPaths(poly)
            print("poly:")
            print(poly[0])
            add_player_poly(poly, pointidx, list_players, list_opponents) #Hinzufügen der Eckpunkte der closed Polygone
        else:
            ridgeidx = 0
            open_polygon_points = []
            field_copy = deepcopy(field)

            for punkte_paar in vor.ridge_points:        ##iteration über die kanten die aus dem punkt gebildet werden
                punkte_paar = np.asarray(punkte_paar)

                if np.any(punkte_paar == pointidx):
                    if min(vor.ridge_vertices[ridgeidx]) >= 0:      ##definierte linien des offenen polygons
                        li = [vor.vertices[vor.ridge_vertices[ridgeidx][0]].tolist(), vor.vertices[vor.ridge_vertices[ridgeidx][1]].tolist()]
                        print()
                        print(li)
                        lines.append([round(li[0]), round(li[1])])
                        val.append(li)

                    else:       ##für offenes polygon
                        center = pointArray.mean(axis=0)
                        v = vor.vertices[vor.ridge_vertices[ridgeidx]][1]  # finite end Voronoi vertex
                        ausgangspunkt1 = pointArray[punkte_paar[1]]
                        ausgangspunkt2 = pointArray[punkte_paar[0]]
                        print(type(ausgangspunkt1))
                        t = ausgangspunkt1 - ausgangspunkt2  # tangent
                        x = np.linalg.norm(t)
                        t = t / x
                        n = np.array([-t[1], t[0]])  # normal
                        midpoint = pointArray[punkte_paar].mean(axis=0)
                        far_point = v + np.sign(np.dot(midpoint - center, n)) * n * 50000
                        p1 = [v[0], v[1]]
                        #if p1 not in open_polygon_points:
                        #    open_polygon_points.append(p1)
                        p2 = [far_point[0], far_point[1]]
                        far_line.append(p2)
                        line = [p1, p2]
                        lines.append(line)
                ridgeidx += 1

        if lines:
            print("Lines: " + str(lines))
            poly = ltp(lines)
            pc = pyclipper.Pyclipper()
            pc.AddPath(field, pyclipper.PT_CLIP, True)
            pc.AddPath(poly, pyclipper.PT_SUBJECT, True)
            poly = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            poly = pyclipper.PolyTreeToPaths(poly)
            if poly:
                poly = poly[0]
            print("\nPoly:")
            print(poly)

            pc = pyclipper.Pyclipper()
            pc.AddPath(field, pyclipper.PT_CLIP, True)
            pc.AddPath(far_line, pyclipper.PT_SUBJECT, False)
            intersect_far = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            intersect_far = pyclipper.PolyTreeToPaths(intersect_far)
            if intersect_far:
                print("\nfucked up poly!")
                intersect_far = intersect_far[0]
                for p in intersect_far:
                    print("intersect_point:" + str(p))
                    idx = poly.index(p)
                    idx2 = idx + 1
                    if idx2 > len(poly) - 1:
                        idx2 = -1
                    if poly[idx2] in intersect_far:
                        iscp = poly[idx - 1]
                    elif poly[idx - 1] in intersect_far:
                        iscp = poly[idx2]
                    for eck in field:
                        if checkPointOnLine(p, [iscp, eck]):
                            poly.pop(idx)
                            poly.insert(idx, eck)
                print(poly)
            add_player_poly(poly, pointidx, list_players, list_opponents)
            #this shit is kinda working

        pointidx += 1

    return val


def add_player_poly(poly, pointidx, list_players, list_opponents):
    polyF = QPolygonF()

    for p in poly:
        polyF.append(QPointF(p[0], p[1]))

    if pointidx > len(list_opponents)-1:
        list_players[pointidx - len(list_opponents)].polygon.setPolygon(polyF)
    else:
        list_opponents[pointidx].polygon.setPolygon(polyF)

