from side_methods.Bewertung import Bewerter


def strat(defender, attacker, scene):
    print("test 1 ")
    positions = attacker.getPosRaster()
    bewerter = Bewerter()
    worst_case_pos = []
    worst_case_pos_str = []
    point_val = {}
    for i in positions:
        val = bewerter.evaluatePoint(i[0], i[1])
        point_val.update({str(i):val})

    #Beachte Worstcase:
    max_val = max(point_val.values())
    #print("Worstcase-Positionen:")
    for point, value in point_val.items():
        if value == max_val:
            worst_case_pos_str.append(point)
    print("test 2 ")
    for i in worst_case_pos_str:
        #Umwandlung String zu Position
        point = i.strip('][').split(', ')
        point[0] = int(point[0])
        point[1] = int(point[1])

        worst_case_pos.append(point)
        #self.worstcase_point = self.scene.addEllipse(point[0],point[1],10,10,QPen(Qt.red),QBrush(Qt.red))
    #print(worst_case_pos)
    enemy_critical_positions = worst_case_pos

    pos = getDefPos(attacker, enemy_critical_positions)
    defender.new_pos = pos
    defender.setLocation(pos[0], pos[1])
    return pos


def getDefPos(attacker, enemy_critical_positions):
    print("test 3 ")
    en_current_pos = attacker.getLocation()
    dxm = round(enemy_critical_positions[0][0] - en_current_pos[0], 2)
    dym = round(enemy_critical_positions[0][1] - en_current_pos[1], 2)

    final_x = en_current_pos[0]+dxm
    final_y = en_current_pos[1]+dym

    # final_pos = [final_x, final_y]
    if final_x < 0:
        """Verschiebung der Finalen Position in eigene Hälfte (nach Strahlensatz)"""
        print("X-Positionierung: " + str(final_x))
        final_pos = [0, final_y - (final_y * final_x/(final_x - 450))]
    else:
        final_pos = [final_x, final_y]

    return final_pos

def advanced(defender, attacker, scene):
    defender.setLocation(defender.new_pos[0], defender.new_pos[1])
    return