from scipy.spatial import Voronoi
from PyQt5.QtGui import QBrush, QPen, QPolygon, QPolygonF
from PyQt5.QtCore import QPoint
import numpy as np
import pyclipper
import polygonSplitter
import math
from sortPolygons import counterClockwise
from copy import deepcopy

def voronoi_function(list_players, list_opponents, field):

    points = []
    for o in list_opponents:
        points.append(o.getLocation())
    for p in list_players:
        points.append(p.getLocation())

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
        ve_schnitt = []
        regions = vor.regions
        regionidx = vor.point_region.tolist()[pointidx]
        print("\n\n")
        print(pointidx)
        print(vor.points[pointidx])
        print(regions[regionidx])
        if min(regions[regionidx], default=-1) >= 0:        ##behandlung falls polygon geschlossen
            for vidx in regions[regionidx]:
                vertex = QPoint(vor.vertices[vidx][0], vor.vertices[vidx][1])
                if pointidx > len(list_opponents)-1:
                    pidx = pointidx - len(list_opponents)
                    list_players[pidx].polygon.append(vertex)
                else:
                    pidx = pointidx
                    list_opponents[pidx].polygon.append(vertex) #Hinzufügen der Eckpunkte der closed Polygone
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
                        lines.append(li)
                        val.append(li)

                    else:       ##für offenes polygon
                        center = pointArray.mean(axis=0)
                        v = vor.vertices[vor.ridge_vertices[ridgeidx]][1]  # finite end Voronoi vertex
                        ausgangspunkt1 = pointArray[punkte_paar[1]]
                        ausgangspunkt2 = pointArray[punkte_paar[0]]
                        t = ausgangspunkt1 - ausgangspunkt2  # tangent
                        x = np.linalg.norm(t)
                        t = t / x
                        n = np.array([-t[1], t[0]])  # normal
                        midpoint = pointArray[punkte_paar].mean(axis=0)
                        far_point = v + np.sign(np.dot(midpoint - center, n)) * n * 5000
                        p1 = [int(v[0]), int(v[1])]
                        #if p1 not in open_polygon_points:
                        #    open_polygon_points.append(p1)
                        p2 = [int(far_point[0]), int(far_point[1])]
                        line = [p1, p2]

                        #Clipping der unendlichen linien
                        pc = pyclipper.Pyclipper()
                        #print("Field: " + str(field))
                        #print("Line: " + str(line))
                        pc.AddPath(field, pyclipper.PT_CLIP, True)
                        pc.AddPath(line, pyclipper.PT_SUBJECT, False)
                        line_intersected = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
                        line_differenced = pc.Execute2(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
                        line_intersected = pyclipper.PolyTreeToPaths(line_intersected)
                        line_differenced = pyclipper.PolyTreeToPaths(line_differenced)
                        s = [i for i in line_intersected[0] if i in line_differenced[0]]
                        lines.append([p1, s[0]])
                        val.append([p1, s[0]])
                        schnittpunkte.append(s[0])
                        #ve_schnitt = ve_schnitt.append(line[0])
                        #if line_intersected:
                        #    lines.append(line_intersected[0])
                        #if solution[0][0] not in field_copy:
                ridgeidx += 1

        print("Lines: " + str(lines))
        ## erstellen von 2 polygonen aus vertices, field und schnittpunkten
        if len(schnittpunkte) > 0:
            print("\n Schnittpunkte: " + str(schnittpunkte))
            possible_polygons = polygonSplitter.splitPolygon(schnittpunkte, field)
            if not possible_polygons:
                ##if schnittpunkte are on same line
                polygon = schnittpunkte

                while len(lines) > 0:
                    for l in lines:
                        if len(lines) == 1:
                            if l == [polygon[0], polygon[1]] or l == [polygon[1], polygon[0]]:
                                lines.remove(l)
                                print("x")
                            else:
                                print("\n!!!!\nSOMETHING WRONG\n!!!\n")
                                print(lines)
                                print(polygon)
                                lines.remove(l)
                                break

                        else:
                            if l[0] == polygon[1]:
                                polygon.insert(1, l[1])
                                lines.remove(l)
                            elif l[1] == polygon[1]:
                                polygon.insert(1, l[0])
                                lines.remove(l)

                print("Polygon: " + str(polygon))

                for p in polygon:
                    print(p)
                    if pointidx > len(list_opponents)-1:
                        pidx = pointidx - len(list_opponents)
                        list_players[pidx].polygon.append(QPoint(p[0], p[1]))
                        print("p added player" + str(pidx))
                    else:
                        pidx = pointidx
                        list_opponents[pidx].polygon.append(QPoint(p[0], p[1]))
                        print("p added op" + str(pidx))

            else:
                ##adding vertices in between schnittpunkte
                first_poly = possible_polygons[0]
                second_poly = possible_polygons[1]
                print("FirstPoly: " + str(first_poly))
                print("SecondPoly: " + str(second_poly))
#                firstPoly = QPolygon(firstPoly)
#                secondPoly = QPolygon(secondPoly)
#                if firstPoly.containsPoint(point.tolist(), Qt_FillRule=1):
#                    print(1)
#                    open_polygon_points = firstPoly
#                else:
#                    print(2)
#                    open_polygon_points = secondPoly

        pointidx += 1

    return val


