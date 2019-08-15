from scipy.spatial import Voronoi
from PyQt5.QtCore import QPoint
import numpy as np
import pyclipper

def voronoi_function(list_players, list_opponents, field):

    points = []
    for p in list_players:
        points.append(p.getLocation())
    for o in list_opponents:
        points.append(o.getLocation())

    pointArray = np.asarray(points)
    vor = Voronoi(pointArray)
    vertices = vor.ridge_vertices
    eckpunkte = vor.vertices
    print("Points: " + str(vor.points))
    print("Ridge_Vertices: " + str(vertices))
    print("Vertices: " + str(eckpunkte))
    print("Ridge_Points: " + str(vor.ridge_points))
    print("Regions: " + str(vor.regions))
    print("Point_regions" + str(vor.point_region))


    lines = []
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            l = [vor.vertices[simplex[0]].tolist(), vor.vertices[simplex[1]].tolist()]
            lines.append(l)

    center = pointArray.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            pc = pyclipper.Pyclipper()
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex
            t = pointArray[pointidx[1]] - pointArray[pointidx[0]]  # tangent
            x = np.linalg.norm(t)
            t = t / x
            n = np.array([-t[1], t[0]])  # normal
            midpoint = pointArray[pointidx].mean(axis=0)
            far_point = vor.vertices[i] + np.sign(np.dot(midpoint - center, n)) * n * 5000
            p1 = [int(vor.vertices[i, 0]), int(vor.vertices[i, 1])]
            p2 = [int(far_point[0]), int(far_point[1])]
            line = [p1, p2]

            #Clipping der unendlichen linien
            print("Field: " + str(field))
            print("Line: " + str(line))
            pc.AddPath(field, pyclipper.PT_CLIP, True)
            pc.AddPath(line, pyclipper.PT_SUBJECT, False)
            solution = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
            solution = pyclipper.PolyTreeToPaths(solution)
            print("solution: " + str(solution))
            print("\n\nlen(Op): " + str(len(list_opponents)) + "\n")
            if solution:
                lines.append(solution[0])

            #Speichern der Polygone für jeden spieler




    return lines
