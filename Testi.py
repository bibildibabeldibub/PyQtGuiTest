
def checkNext(unterkante, all_schatten, pos):
    """
    :param unterkante:
    :param all_schatten:
    :param pos:
    :return: neue Unterkante & Position des letzten betroffenen Elements
    """
    if unterkante < all_schatten[pos][0]:
        """Unterkante reicht nicht bis in den nächsten Schatten"""
        return unterkante, pos -1
    elif unterkante < all_schatten[pos][1]:
        """Unterkante reicht bis in diesen Schatten"""
        return all_schatten[pos][1], pos
    else:
        if pos +1 < len(all_schatten):
            """Unterkante könnte in nächsten Schatten reichen"""
            return checkNext(unterkante, all_schatten, pos +1)
        else:
            """Unterkante letzte untere Kante"""
            return unterkante, pos

def Test(tor_schatten_oben, tor_schatten_unten, schatten):
    pos = 0
    pos_dif = None
    for s in schatten:
        if tor_schatten_oben < s[0]:
            """Oberkante befindet sich über alter Kante"""
            if tor_schatten_unten < s[0]:
                """neuer Schatten komplett über bestehendem"""
                schatten.insert(pos, [tor_schatten_oben, tor_schatten_unten])
                break
            elif s[0] <= tor_schatten_unten <= s[1]:
                """neuer Schatten schneidet bestehendem -> Aktualisierung Oberkante"""
                s[0] = tor_schatten_oben
                break
            elif s[1] <= tor_schatten_unten:
                """neuer Schatten überlagert bestehenden"""
                unterkanten_wert, pos_dif = checkNext(tor_schatten_unten, schatten, pos+1)
                s[0] = tor_schatten_oben
                s[1] = unterkanten_wert
                break

        elif s[0] <= tor_schatten_oben <= s[1]:
            """Oberkante des neuen Schattens befindet sich in bestehendem Schatten"""
            if s[1] < tor_schatten_unten:
                """ersetzen der unteren Schattenkante"""
                unterkanten_wert, pos_dif = checkNext(tor_schatten_unten, schatten, pos+1)
                s[1] = unterkanten_wert
                break
            else:
                """Schatten wird bereits verdeckt"""
                break
        elif pos == len(schatten) - 1:
            schatten.append([tor_schatten_oben, tor_schatten_unten])
            break
        pos += 1

    if pos_dif:
        for p in range(pos, pos_dif):
            """Entfernen überschatteter Schattenelemente
            pos ist das bearbeite Element 
            pos_dif ist das letzte überschattete Element"""
            schatten.pop(pos+1)
