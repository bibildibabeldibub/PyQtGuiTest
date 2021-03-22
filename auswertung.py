import os
import json
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import statistics
import math
import numpy as np

def mittelwert(liste):
    n = 0
    s = 0
    for x in liste:
        s += x
        n += 1

    return s/n

def standardabweichung(liste):
    v = statistics.variance(liste)
    return math.sqrt(v)


def auswerten(directory):
    """
    Auswertung der Ergebnisse
    :param directory: Ordner in dem sich die ergebnisse befinden
    :return: Positionen der Extremalwerte für ohne und mit Bonus/Malus
    """
    logdir = "log"
    ohne_first = []
    schuss_first = []
    block_first = []
    beides_first = []

    ohne_second = []
    schuss_second = []
    block_second = []
    beides_second = []

    strats = []

    minimum_first_ohne = 32000
    minimum_second_ohne = 32000
    minimum_first_beides = 32000
    minimum_second_beides = 32000

    maximum_first_ohne = 0
    maximum_second_ohne = 0
    maximum_first_beides = 0
    maximum_second_beides = 0

    minimum_first_file_ohne = [""]
    minimum_second_file_ohne = [""]
    minimum_first_file_beides = [""]
    minimum_second_file_beides = [""]

    maximum_first_file_ohne = [""]
    maximum_second_file_ohne = [""]
    maximum_first_file_beides = [""]
    maximum_second_file_beides = [""]


    directories = os.listdir(logdir)
    directories.remove("excluded")
    directories.remove("test")

    for x in directories:
        if x == "excluded" or x == "test":
            continue
        print(str(directories.index(x)) + ". " + x)
    print(str(len(directories))+". Exit")

    if not directory:
        while True:
            try:
                eingabe = int(input("\nOrdner zum Auswerten wählen: "))
                if eingabe == len(directories):
                    exit()
                break
            except ValueError:
                print("Bitte Ordner-Nummer angeben!")

        logdir = os.path.join(logdir, directories[eingabe])
    else:
        logdir = os.path.join(logdir, directory)
    print(logdir)
    ######################## Gathering #######################
    for date in os.listdir(logdir):
        date_path = os.path.join(logdir, date)

        for setup in os.listdir(date_path):
            setup_path = os.path.join(date_path, setup)
            for strat in os.listdir(setup_path):
                if strat == "start":
                    continue
                strats.append(strat)
                file_path = os.path.join(setup_path, strat)
                with open(file_path, 'r') as js:
                    js = js.read()
                    data = json.loads(js)
                    scores = data["Scores"]
                    if not scores.keys():
                        exit("Keine Scores in Datei: " + os.path.join(setup_path, strat))

                    for k in scores.keys():
                        if strats.index(strat) == 0:
                            '''Strategie 1'''
                            ohne_first.append(scores[k]["ohne"])
                            '''Sammeln von Extrema'''
                            #Minimum ohne
                            if scores[k]["ohne"] < minimum_first_ohne:
                                minimum_first_ohne = scores[k]["ohne"]
                                minimum_first_file_ohne = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == minimum_first_ohne:
                                minimum_first_file_ohne.append(file_path + "/" + str(k))
                            #Maximum ohne
                            if scores[k]["ohne"] > maximum_first_ohne:
                                maximum_first_ohne = scores[k]["ohne"]
                                maximum_first_file_ohne = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == maximum_first_ohne:
                                maximum_first_file_ohne.append(file_path + "/" + str(k))
                            #Minimum beides
                            if scores[k]["beides"] < minimum_first_beides:
                                minimum_first_beides = scores[k]["beides"]
                                minimum_first_file_beides = [file_path + "/" + str(k)]
                            elif scores[k]["beides"] == minimum_first_beides:
                                minimum_first_file_beides.append(file_path + "/" + str(k))
                            #Maximum beides
                            if scores[k]["beides"] > maximum_first_beides:
                                maximum_first_beides = scores[k]["beides"]
                                maximum_first_file_beides = [file_path + "/" + str(k)]
                            elif scores[k]["beides"] == maximum_first_beides:
                                maximum_first_file_beides.append(file_path + "/" + str(k))

                            schuss_first.append(scores[k]["schussweg"])
                            block_first.append(scores[k]["spieler"])
                            beides_first.append(scores[k]["beides"])
                        elif strats.index(strat) == 1:
                            '''Strategie 2'''
                            ohne_second.append(scores[k]["ohne"])
                            '''Tracking von min und max Werten'''
                            #Ohne minimum
                            if scores[k]["ohne"] < minimum_second_ohne:
                                minimum_second_ohne = scores[k]["ohne"]
                                minimum_second_file_ohne = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == minimum_second_ohne:
                                minimum_second_file_ohne.append(file_path + "/" + str(k))
                            #ohne Maximim
                            if scores[k]["ohne"] > maximum_second_ohne:
                                maximum_second_ohne = scores[k]["ohne"]
                                maximum_second_file_ohne = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == maximum_second_ohne:
                                maximum_second_file_ohne.append(file_path + "/" + str(k))
                            #beides Minimum
                            if scores[k]["beides"] < minimum_second_beides:
                                minimum_second_beides = scores[k]["beides"]
                                minimum_second_file_beides = [file_path + "/" + str(k)]
                            elif scores[k]["beides"] == minimum_second_beides:
                                minimum_second_file_beides.append(file_path + "/" + str(k))
                            #Beides Maximum
                            if scores[k]["beides"] > maximum_second_beides:
                                maximum_second_beides = scores[k]["beides"]
                                maximum_second_file_beides = [file_path + "/" + str(k)]
                            elif scores[k]["beides"] == maximum_second_beides:
                                maximum_second_file_beides.append(file_path + "/" + str(k))

                            schuss_second.append(scores[k]["schussweg"])
                            block_second.append(scores[k]["spieler"])
                            beides_second.append(scores[k]["beides"])

    print(len(ohne_first))
    print(len(ohne_second))

    print("Shapiro-Wilk-Test: Base-Ohne (W, P)")
    sw_ob = stats.shapiro(ohne_first)
    print(type(sw_ob))
    print(sw_ob)
    print("\n")

    print("Shapiro-Wilk-Test: Naiv-Ohne (W, P)")
    sw_on = stats.shapiro(ohne_second)
    print(sw_on)
    print("\n")

    print("Shapiro-Wilk-Test: Base-Schussweg (W, P)")
    sw_sb = stats.shapiro(schuss_first)
    print(sw_sb)
    print("\n")

    print("Shapiro-Wilk-Test: Naiv-Schussweg (W, P)")
    sw_sn = stats.shapiro(schuss_second)
    print(sw_sn)
    print("\n")

    print("Shapiro-Wilk-Test: Base-Spielerblock (W, P)")
    sw_bb = stats.shapiro(block_first)
    print(sw_bb)
    print("\n")

    print("Shapiro-Wilk-Test: Naiv-Spielerblock (W, P)")
    sw_bn = stats.shapiro(block_second)
    print(sw_bn)
    print("\n")

    print("Shapiro-Wilk-Test: Base-Beides (W, P)")
    sw_bothb = stats.shapiro(beides_first)
    print(sw_bothb)
    print("\n")

    print("Shapiro-Wilk-Test: Naiv-Beides (W, P)")
    sw_bothn = stats.shapiro(beides_second)
    print(sw_bothn)
    print("\n")

    parts = []
    if strats[1] == 'first':
        strats[1] = 'naiv'

    fig1, axes1 = plt.subplots(ncols=2, sharey='all')
    fig1.canvas.set_window_title("Ohne Bonus/Malus")
    axes1[0].set_title(strats[0] + " SW-Test(W): " + str(round(sw_ob[0], 3)))
    axes1[0].set_ylabel("Bewertung")
    parts.append(axes1[0].violinplot(ohne_first, showextrema=True, showmeans=True, showmedians=False))
    axes1[1].set_title(strats[1] + " SW-Test(W): " + str(round(sw_on[0], 3)))
    parts.append(axes1[1].violinplot(ohne_second, showextrema=True, showmeans=True, showmedians=False))

    # fig2, axes2 = plt.subplots(ncols=2, sharey='all')
    # fig2.canvas.set_window_title("Schussweg Malus")
    # axes2[0].set_title(strats[0] + " SW-Test(W): " + str(round(sw_sb[0], 3)))
    # axes2[0].set_ylabel("Bewertung")
    # parts.append(axes2[0].violinplot(schuss_first, showextrema=True, showmeans=True, showmedians=False))
    # axes2[1].set_title(strats[1] + " SW-Test(W): " + str(round(sw_sn[0], 3)))
    # parts.append(axes2[1].violinplot(schuss_second, showextrema=True, showmeans=True, showmedians=False))
    #
    # fig3, axes3 = plt.subplots(ncols=2, sharey='all')
    # fig3.canvas.set_window_title("Block Bonus")
    # axes3[0].set_title(strats[0] + " SW-Test(W): " + str(round(sw_bb[0], 3)))
    # axes3[0].set_ylabel("Bewertung")
    # parts.append(axes3[0].violinplot(block_first, showextrema=True, showmeans=True, showmedians=False))
    # axes3[1].set_title(strats[1] + " SW-Test(W): " + str(round(sw_bn[0], 3)))
    # parts.append(axes3[1].violinplot(block_second, showextrema=True, showmeans=True, showmedians=False))


    fig4, axes4 = plt.subplots(ncols=2, sharey='all')
    fig4.canvas.set_window_title("Beides")
    axes4[0].set_title(strats[0] + " SW-Test(W): " + str(round(sw_bothb[0], 3)))
    axes4[0].set_ylabel("Bewertung")
    parts.append(axes4[0].violinplot(beides_first, showextrema=True, showmeans=True, showmedians=False))
    axes4[1].set_title(strats[1] + " SW-Test(W): " + str(round(sw_bothn[0], 3)))
    parts.append(axes4[1].violinplot(beides_second, showextrema=True, showmeans=True, showmedians=False))


    for p in parts:
        for pc in p['bodies']:
            pc.set_edgecolor('black')

    plt.subplots_adjust(bottom=0.15, wspace=0.05)
    plt.show()

    if not os.path.exists('plots'):
        os.mkdir('plots')
    # t = datetime.datetime.now()
    # t = t.strftime("%d_%m_%Y-%H_%M_%S")

    t = logdir + "_" + strats[0] + "-" + strats[1]

    # if not os.path.isdir(os.path.join("plots", t)):
    #     os.mkdir(os.path.join("plots", t))

    # fig1.savefig(os.path.join("plots", t, "ohne"))
    # fig2.savefig(os.path.join("plots", t, "schussweg"))
    # fig3.savefig(os.path.join("plots", t, "angreifer_blockierung"))
    # fig4.savefig(os.path.join("plots", t, "beides"))

    result = {}
    min_of = "Minimum " + strats[0] + " - Ohne"
    print(minimum_first_file_ohne)
    result.update({min_of: minimum_first_file_ohne})

    min_os = "Minimum " + strats[1] + " - Ohne"
    print(minimum_second_file_ohne)
    result.update({min_os: minimum_second_file_ohne})

    min_bf = "Minimum " + strats[0] + " - Beides"
    print(minimum_first_file_beides)
    result.update({min_bf: minimum_first_file_beides})

    min_bs = "Minimum " + strats[1] + " - Beides"
    print(minimum_second_file_beides)
    result.update({min_bs: minimum_second_file_beides})

    max_of = "Maximum " + strats[0] + " - Ohne"
    print(maximum_first_file_ohne)
    result.update({max_of: maximum_first_file_ohne})

    max_os = "Maximum " + strats[1] + " - Ohne"
    print(maximum_second_file_ohne)
    result.update({max_os: maximum_second_file_ohne})

    max_bf = "Maximum " + strats[0] + " - Beides"
    print(maximum_first_file_beides)
    result.update({max_bf: maximum_first_file_beides})

    max_bs = "Maximum " + strats[1] + " - Beides"
    print(maximum_second_file_beides)
    result.update({max_bs: maximum_second_file_beides})

    return result
