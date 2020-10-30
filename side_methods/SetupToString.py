

def getString(dict_players, dict_opponents):
    txt = ""
    for p in dict_players:
        txt += str(p)
    txt += "Opponents:\n"
    for x in dict_opponents:
        txt += str(x) + "\n"
    print('\n' + txt)

    return txt
