
def checkPointOnLine(point, line):
    dxc = point[0] - line[0][0]
    dyc = point[1] - line[0][1]

    dxl = line[0][0] - line[1][0]
    dyl = line[0][1] - line[1][1]

    cross = dxc * dyl - dyc * dxl
    val = cross == 0
    return val