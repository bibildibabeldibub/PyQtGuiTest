from scipy.spatial import Voronoi, voronoi_plot_2d


def voronoi_function(dict_players, dict_opponents):
    """taking all players and returning list of voronoi lines (list of quadruples x1,y1,x2,y2) """
    print("\n\n\nVoronoi:")
    eckpunkte = []
    ridges = []
    #points = [[-450, -300], [450, -300], [1350, -300],
    #          [-450, 300], [450, 300 ], [1350, 300],
    #          [-450, 900], [450, 900 ], [1350, 900]]
    points = []
    for p in dict_players:
        points.append(p.getLocation())
    for o in dict_opponents:
        points.append(o.getLocation())
    vor = Voronoi(points)
    eckpunkte = vor.vertices
    ridges = vor.ridge_vertices

    print("länge rigdes: " + str(len(ridges)))
    print("ridges: " + str(ridges))
    print("Vertices: " + str(eckpunkte))
    lines = []
    for vpair in ridges:
        if vpair[0] >= 0 and vpair[1] >= 0:
            v0 = eckpunkte[vpair[0]]
            v1 = eckpunkte[vpair[1]]
            lines.append([round(v0[0], 2), round(v0[1], 2), round(v1[0], 2), round(v1[1], 2)])

    return lines


