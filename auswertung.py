import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

logdir = "log"
ohne_base = []
schuss_base = []
block_base = []
beides_base = []

ohne_naiv = []
schuss_naiv = []
block_naiv= []
beides_naiv = []

for date in os.listdir(logdir):
    date_path = os.path.join(logdir, date)
    for setup in os.listdir(date_path):
        setup_path = os.path.join(date_path, setup)
        for strat in os.listdir(setup_path):
            if strat != "start":
                with open(os.path.join(setup_path, strat), 'r') as js:
                    js = js.read()
                    data = json.loads(js)
                    scores = data["Scores"]
                    if not scores.keys():
                        exit("Keine Scores in Datei: " + os.path.join(setup_path, strat))

                    for k in scores.keys():
                        if strat == 'base':
                            ohne_base.append(scores[k]["ohne"])
                            schuss_base.append(scores[k]["schussweg"])
                            block_base.append(scores[k]["spieler"])
                            beides_base.append(scores[k]["beides"])
                        elif strat == 'first':
                            ohne_naiv.append(scores[k]["ohne"])
                            schuss_naiv.append(scores[k]["schussweg"])
                            block_naiv.append(scores[k]["spieler"])
                            beides_naiv.append(scores[k]["beides"])

print(len(ohne_naiv))
print(len(ohne_base))
print(len(schuss_naiv))
print(len(schuss_base))
print(len(block_naiv))
print(len(block_base))
print(len(beides_naiv))
print(len(beides_base))
#zur Darstellung mehrerer Daten wird

fig1, ax1 = plt.subplots()
ax1.set_title('Ohne Bonus/Malus')
ax1.boxplot([ohne_base, ohne_naiv])

fig2, ax2 = plt.subplots()
ax2.set_title('Schussweg Malus')
ax2.boxplot([schuss_base, schuss_naiv])

fig3, ax3 = plt.subplots()
ax3.set_title('Blockierung Bonus')
ax3.boxplot([block_base, block_naiv])

fig4, ax4 = plt.subplots()
ax4.set_title('Bonus und Malus')
ax4.boxplot([beides_base, beides_naiv])


if not os.path.exists('plots'):
    os.mkdir('plots')
t = datetime.datetime.now()
t = t.strftime("%d_%m_%Y-%H_%M_%S")

if not os.path.isdir(os.path.join("plots", t)):
    os.mkdir(os.path.join("plots", t))

plt.savefig(os.path.join("plots", t, "ohne"))
plt.savefig(os.path.join("plots", t, "schussweg"))
plt.savefig(os.path.join("plots", t, "angreifer_blockierung"))
plt.savefig(os.path.join("plots", t, "beides"))


