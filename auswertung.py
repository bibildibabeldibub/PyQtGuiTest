import os
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

logdir = "log"
ohne = []
schuss = []
block = []
beides = []

for f in os.listdir(logdir):
    with open(os.path.join(logdir, f), 'r') as j:
        j = j.read()
        data = json.loads(j)
        scores = data["Scores"]
        if not scores.keys():
            exit("Keine Scores in Datei: " + f)

        for k in scores.keys():
            ohne.append(scores[k]["ohne"])
            schuss.append(scores[k]["schussweg"])
            block.append(scores[k]["spieler"])
            beides.append(scores[k]["beides"])

print("Ohne:\n\t")
print(ohne)
print("Schussweg:\n\t")
print(schuss)
print("Spielerblock:\n\t")
print(block)
print("Beides :\n\t")
print(beides)

#zur Darstellung mehrerer Daten wird

fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(ohne)

if not os.path.exists('plots'):
    os.mkdir('plots')
t = datetime.datetime.now()
t = t.strftime("%d_%m_%Y-%H_%M_%S")
plt.savefig('plots/' + t)


