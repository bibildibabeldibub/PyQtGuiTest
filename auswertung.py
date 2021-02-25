import os
import json
import datetime
import matplotlib.pyplot as plt
from scipy import stats

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

p_wert_ohne = stats.ttest_ind(ohne_base, ohne_naiv)[1]
print(len(ohne_naiv))
print(len(ohne_base))
print("P-Wert:" + str(p_wert_ohne))

p_wert_schuss = stats.ttest_ind(schuss_base, schuss_naiv)[1]
print(len(schuss_naiv))
print(len(schuss_base))
print("P-Wert:" + str(p_wert_schuss))

p_wert_block = stats.ttest_ind(block_base, block_naiv)[1]
print(len(block_naiv))
print(len(block_base))
print("P-Wert:" + str(p_wert_block))

p_wert_beides = stats.ttest_ind(beides_base, beides_naiv)[1]
print(len(beides_naiv))
print(len(beides_base))
print("P-Wert:" + str(p_wert_beides))
#zur Darstellung mehrerer Daten wird


fig1, ax1 = plt.subplots()
ax1.set_title('Ohne Bonus/Malus :  ' + str(p_wert_ohne))
ax1.boxplot([ohne_base, ohne_naiv])

fig2, ax2 = plt.subplots()
ax2.set_title('Schussweg Malus :  ' + str(p_wert_schuss))
ax2.boxplot([schuss_base, schuss_naiv])

fig3, ax3 = plt.subplots()
ax3.set_title('Blockierung Bonus :  ' + str(p_wert_block))
ax3.boxplot([block_base, block_naiv])

fig4, ax4 = plt.subplots()
ax4.set_title('Bonus und Malus :  ' + str(p_wert_beides))
ax4.boxplot([beides_base, beides_naiv])

plt.show()


if not os.path.exists('plots'):
    os.mkdir('plots')
t = datetime.datetime.now()
t = t.strftime("%d_%m_%Y-%H_%M_%S")

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


