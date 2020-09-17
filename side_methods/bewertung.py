import math

def evaluate_point(x: float, y: float):
        """:returns Wert an dem Punkt"""
        # print("\n--------------------")
        # print("Mittelpunkt: " + str(x) + "|" + str(y) )
        dx = 450 - x
        dy = 0 - y
        distance = math.sqrt(dx*dx+dy*dy)
        wert = 100/distance
        # print("Distanz:" + str(distance))
        # print("Wert:" + str(wert))
        return wert
