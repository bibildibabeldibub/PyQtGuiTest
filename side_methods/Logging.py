import os
from side_methods import LinesToPolygon, SetupToString, Bewertung
from datetime import datetime


def writeLog(app, situation, wiederholung):
    if not app.log:
        print("Simple Anim, No log created")
        return

    print("\nStart logging -- " + situation)
    app.date = app.t.strftime("%d_%m_%Y_%H_%M_%S")
    path = app.temppath + app.date + "/" + "run-" + str(wiederholung)
    new = situation+":\n"
    new += SetupToString.getString(app.dict_defenders, app.dict_attackers)

    if situation == "Ende" or situation == "Nach 5 Sekunden" or situation == "Nach 10 Sekunden":
        print("Bewertungsberechnung...")
        new += Bewertung.evaluateScene(app.scene)

    #Create Folderstructure if not exists
    if not os.path.exists("log"):
        os.mkdir("log")
    if not os.path.exists(app.temppath):
        os.mkdir(app.temppath)
    if not os.path.exists(app.temppath + app.date):
        os.mkdir(app.temppath + app.date)

    if os.path.isfile(path):
        f = open(path, 'a')
        t = open(path)
        t = t.read()
        print(t+new)
        f.write(new)

    else:
        f = open(path, 'w')
        f.write(new)

class JsonLogger(object):
    def __init__(self):
        date = datetime.now()
        self.path = date.strftime("%d_%m_%Y_%H_%M_%S")
        self.path = "log/" + self.path + ".json"

        if not os.path.exists("log"):
            os.mkdir("log")

    def getText(self):
        file = open(self.path, 'r')
        text = file.read()
        return text

    def writeText(self, text):
        file = open(self.path, 'w')
        file.write(text)
        file.close()

    def clearFile(self):
        file = open(self.path, 'w')
        file.close()
