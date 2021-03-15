import os
import json
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import statistics
import math

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

logdir = "log"
ohne_base = []
schuss_base = []
block_base = []
beides_base = []

ohne_naiv = []
schuss_naiv = []
block_naiv= []
beides_naiv = []

minimum_base = 32000
minimum_base_file = [""]

minimum_first = 32000
minimum_first_file = [""]

for date in os.listdir(logdir):
    date_path = os.path.join(logdir, date)
    if date == 'excluded':
        continue
    for setup in os.listdir(date_path):
        setup_path = os.path.join(date_path, setup)
        for strat in os.listdir(setup_path):
            if strat != "start":
                file_path = os.path.join(setup_path, strat)
                with open(file_path, 'r') as js:
                    js = js.read()
                    data = json.loads(js)
                    scores = data["Scores"]
                    if not scores.keys():
                        exit("Keine Scores in Datei: " + os.path.join(setup_path, strat))

                    for k in scores.keys():
                        if strat == 'base':
                            ohne_base.append(scores[k]["ohne"])
                            if scores[k]["ohne"] < minimum_base:
                                minimum_base = scores[k]["ohne"]
                                minimum_base_file = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == minimum_base:
                                minimum_base_file.append(file_path + "/" + str(k))

                            schuss_base.append(scores[k]["schussweg"])
                            block_base.append(scores[k]["spieler"])
                            beides_base.append(scores[k]["beides"])
                        elif strat == 'first':
                            ohne_naiv.append(scores[k]["ohne"])
                            if scores[k]["ohne"] < minimum_base:
                                minimum_first = scores[k]["ohne"]
                                minimum_first_file = [file_path + "/" + str(k)]
                            elif scores[k]["ohne"] == minimum_base:
                                minimum_first_file.append(file_path + "/" + str(k))

                            schuss_naiv.append(scores[k]["schussweg"])
                            block_naiv.append(scores[k]["spieler"])
                            beides_naiv.append(scores[k]["beides"])

print(len(ohne_base))
print(len(ohne_naiv))

print("Shapiro-Wilk-Test: Base-Ohne (W, P)")
sw_ob = stats.shapiro(ohne_base)
print(type(sw_ob))
print(sw_ob)
print("\n")

print("Shapiro-Wilk-Test: Naiv-Ohne (W, P)")
sw_on = stats.shapiro(ohne_naiv)
print(sw_on)
print("\n")

print("Shapiro-Wilk-Test: Base-Schussweg (W, P)")
sw_sb = stats.shapiro(schuss_base)
print(sw_sb)
print("\n")

print("Shapiro-Wilk-Test: Naiv-Schussweg (W, P)")
sw_sn = stats.shapiro(schuss_naiv)
print(sw_sn)
print("\n")

print("Shapiro-Wilk-Test: Base-Spielerblock (W, P)")
sw_bb = stats.shapiro(block_base)
print(sw_bb)
print("\n")

print("Shapiro-Wilk-Test: Naiv-Spielerblock (W, P)")
sw_bn = stats.shapiro(block_naiv)
print(sw_bn)
print("\n")

print("Shapiro-Wilk-Test: Base-Beides (W, P)")
sw_bothb = stats.shapiro(beides_base)
print(sw_bothb)
print("\n")

print("Shapiro-Wilk-Test: Naiv-Beides (W, P)")
sw_bothn = stats.shapiro(beides_naiv)
print(sw_bothn)
print("\n")

parts = []

fig1, axes1 = plt.subplots(ncols=2, sharey='all')
fig1.canvas.set_window_title("Ohne Bonus/Malus")
axes1[0].set_title("Base SW-Test(W): " + str(round(sw_ob[0], 3)))
axes1[0].set_ylabel("Bewertung")
parts.append(axes1[0].violinplot(ohne_base, showextrema=True, showmeans=True, showmedians=True))
axes1[1].set_title("Naiv SW-Test(W): " + str(round(sw_on[0], 3)))
parts.append(axes1[1].violinplot(ohne_naiv, showextrema=True, showmeans=True, showmedians=True))

fig2, axes2 = plt.subplots(ncols=2, sharey='all')
fig2.canvas.set_window_title("Schussweg Malus")
axes2[0].set_title("Base SW-Test(W): " + str(round(sw_sb[0], 3)))
axes2[0].set_ylabel("Bewertung")
parts.append(axes2[0].violinplot(schuss_base, showextrema=True, showmeans=True, showmedians=True))
axes2[1].set_title("Naiv SW-Test(W): " + str(round(sw_sn[0], 3)))
parts.append(axes2[1].violinplot(schuss_naiv, showextrema=True, showmeans=True, showmedians=True))

fig3, axes3 = plt.subplots(ncols=2, sharey='all')
fig3.canvas.set_window_title("Block Bonus")
axes3[0].set_title("Base SW-Test(W): " + str(round(sw_bb[0], 3)))
axes3[0].set_ylabel("Bewertung")
parts.append(axes3[0].violinplot(block_base, showextrema=True, showmeans=True, showmedians=True))
axes3[1].set_title("Naiv SW-Test(W): " + str(round(sw_bn[0], 3)))
parts.append(axes3[1].violinplot(block_naiv, showextrema=True, showmeans=True, showmedians=True))

fig4, axes4 = plt.subplots(ncols=2, sharey='all')
fig4.canvas.set_window_title("Beides")
axes4[0].set_title("Base SW-Test(W): " + str(round(sw_bothb[0], 3)))
axes4[0].set_ylabel("Bewertung")
parts.append(axes4[0].violinplot(beides_base, showextrema=True, showmeans=True, showmedians=True))
axes4[1].set_title("Naiv SW-Test(W): " + str(round(sw_bothn[0], 3)))
parts.append(axes4[1].violinplot(beides_naiv, showextrema=True, showmeans=True, showmedians=True))


for p in parts:
    for pc in p['bodies']:
        pc.set_edgecolor('black')

# val = stats.ttest_ind(ohne_base, ohne_naiv, equal_var=False)
# t_wert_ohne = val[0]
# p_wert_ohne = val[1]
# # print(len(ohne_naiv))
# # print(len(ohne_base))
# print("Ohne:")
# print("\tP-Wert:" + str(p_wert_ohne))
# print("\tT-Wert:" + str(t_wert_ohne))
# print("\tMittelwert-base:" + str(mittelwert(ohne_base)))
# print("\tMittelwert-naiv:" + str(mittelwert(ohne_naiv)))
# print("\tStandardabweichung-base:" + str(standardabweichung(ohne_base)))
# print("\tStandardabweichung-naiv:" + str(standardabweichung(ohne_naiv)))
#
# val = stats.ttest_ind(schuss_base, schuss_naiv, equal_var=False)
# t_wert_schuss = val[0]
# p_wert_schuss = val[1]
# # print(len(schuss_naiv))
# # print(len(schuss_base))
# print("Schussweg")
# print("\tP-Wert:" + str(p_wert_schuss))
# print("\tT-Wert:" + str(t_wert_schuss))
# print("\tMittelwert-base:" + str(mittelwert(schuss_base)))
# print("\tMittelwert-naiv:" + str(mittelwert(schuss_naiv)))
# print("\tStandardabweichung-base:" + str(standardabweichung(schuss_base)))
# print("\tStandardabweichung-naiv:" + str(standardabweichung(schuss_naiv)))
#
# val = stats.ttest_ind(block_base, block_naiv, equal_var=False)
# t_wert_block = val[0]
# p_wert_block = val[1]
# # print(len(block_naiv))
# # print(len(block_base))
# print("Spielerblockierung:")
# print("\tP-Wert:" + str(p_wert_block))
# print("\tT-Wert:" + str(t_wert_block))
# print("\tMittelwert-base:" + str(mittelwert(block_base)))
# print("\tMittelwert-naiv:" + str(mittelwert(block_naiv)))
# print("\tStandardabweichung-base:" + str(standardabweichung(block_base)))
# print("\tStandardabweichung-naiv:" + str(standardabweichung(block_naiv)))
#
# val = stats.ttest_ind(beides_base, beides_naiv, equal_var=False)
# t_wert_beides = val[0]
# p_wert_beides = val[1]
# # print(len(beides_naiv))
# # print(len(beides_base))
# print("Beides:")
# print("\tP-Wert:" + str(p_wert_beides))
# print("\tT-Wert:" + str(t_wert_beides))
# print("\tMittelwert-base:" + str(mittelwert(beides_base)))
# print("\tMittelwert-naiv:" + str(mittelwert(beides_naiv)))
# print("\tStandardabweichung-base:" + str(standardabweichung(beides_base)))
# print("\tStandardabweichung-naiv:" + str(standardabweichung(beides_naiv)))


plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.show()

if not os.path.exists('plots'):
    os.mkdir('plots')
# t = datetime.datetime.now()
# t = t.strftime("%d_%m_%Y-%H_%M_%S")
t = 'violinplots'

if not os.path.isdir(os.path.join("plots", t)):
    os.mkdir(os.path.join("plots", t))

fig1.savefig(os.path.join("plots", t, "ohne"))
fig2.savefig(os.path.join("plots", t, "schussweg"))
fig3.savefig(os.path.join("plots", t, "angreifer_blockierung"))
fig4.savefig(os.path.join("plots", t, "beides"))

print("Minimum Base:")
print(minimum_base_file)
print("Minimum First:")
print(minimum_first_file)


