from scipy.spatial import Voronoi
import numpy as np

def voronoi_function(dict_players, dict_opponents):
    points = []
    for p in dict_players:
        points.append(p.getLocation())
    for o in dict_opponents:
        points.append(o.getLocation())
    print("Points: " + str(points))

    bastard = np.asarray(points)
    vor = Voronoi(bastard)
    vertices = vor.ridge_vertices
    eckpunkte = vor.vertices
    print(bastard)

    lines = []
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            a = vor.vertices[simplex[0]]
            a1 = a.tolist()
            l = [a1, vor.vertices[simplex[1]].tolist()]
            lines.append(l)

    print("\n\nLines:")
    print(len(lines))

    center = bastard.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex
            print("Finite Point: " + str(i))
            t = bastard[pointidx[1]] - bastard[pointidx[0]]  # tangent
            print("Vektor P1P2: " + str(t))
            x = np.linalg.norm(t)
            t = t / x
            n = np.array([-t[1], t[0]])  # normal
            midpoint = bastard[pointidx].mean(axis=0)
            far_point = vor.vertices[i] + np.sign(np.dot(midpoint - center, n)) * n * 100
    
            lines.append([[vor.vertices[i, 0], vor.vertices[i, 1]], [far_point[0], far_point[1]]])

    return lines
