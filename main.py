# This is a sample Python script.
import os
from matplotlib import pyplot as plt
import seaborn as sns
import csv
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    pass
    # Use a breakpoint in the code line below to debug your script.
    #String = autoclass("java.lang.String")
    #Pyworker = autoclass("it.units.erallab.Pyworker")
    #js = String(name)
    #print(Pyworker)

def loadData(filename):
    data = dict()
    # print(filename)
    maxit = -1
    with open(filename, encoding='utf-8') as f:
        fr = csv.DictReader(f, delimiter=";")
        for l in fr:
            it = int(l["event→iterations"])
            fit = -1
            if "individual→fitness→velocity" in fr.fieldnames:
                fit = float(l["individual→fitness→velocity"])
            else:
                fit =float(l["individual→fitness→fitness"])
            if it in data:
                data[it].append(fit)
            else:
                data[it] = [fit]
            maxit = max(it,maxit)
    res = list()
    for i in range(maxit+1):
        res.append(np.max(data[i]))

    return res

def avgData(mat):
    m= list()
    s =list()
    for i in range(len(mat[0])):
        tmp = list()

        for j in range(len(mat)):

            tmp.append(mat[j][i])
        m.append(np.median(tmp))
        s.append(np.std(tmp))
    return m,s

def getBestSer(filename):
    fit =-1.0
    ser = ""
    with open(filename, encoding='utf-8') as f:
        fr = csv.DictReader(f, delimiter=";")
        #(fr.fieldnames)
        field = "individual→fitness→velocity"
        if not "individual→fitness→velocity" in fr.fieldnames:
            field = "individual→fitness→fitness"
        for l in fr:
            if float(l[field])> fit:
                fit = float(l[field])
                ser = l["individual→solution→serialized"]
    return ser

def getBestFitness(filename):
    fit = -1.0
    with open(filename, encoding='utf-8') as f:
        fr = csv.DictReader(f, delimiter=";")
        # (fr.fieldnames)
        field = "individual→fitness→velocity"
        if not "individual→fitness→velocity" in fr.fieldnames:
            field = "individual→fitness→fitness"
        for l in fr:
            if float(l[field]) > fit:
                fit = float(l[field])
    return fit

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    base = list()
    baseh = list()
    baseh01 = list()
    resNoHebbian001 = list()
    resNoHebbian00 = list()
    resNoHebbian10 = list()
    resNoHebbian05 = list()
    resNoHebbian20 = list()
    resNoHebbian75 = list()
    resNoHebbian40 = list()
    resNoHebbian01 = list()
    for i in range(10):
        m = loadData("data/nohes_00_all_"+str(i)+".txt")
        base.append(m)
        m = loadData("data/es_00_all_" + str(i) + ".txt")
        baseh.append(m)
        m = loadData("data/step/hstep01_00_all_" + str(i) + ".txt")
        baseh01.append(m)
        m = loadData("data/step/h01step_25_all_" + str(i) + ".txt")
        resNoHebbian001.append(m)
        m = loadData("data/step/step_25_all_" + str(i) + ".txt")
        resNoHebbian00.append(m)
        m = loadData("data/step/step_50_all_" + str(i) + ".txt")
        resNoHebbian10.append(m)
        m = loadData("data/step/hstep_25_all_" + str(i) + ".txt")
        resNoHebbian05.append(m)
        m = loadData("data/step/hstep_50_all_" + str(i) + ".txt")
        resNoHebbian75.append(m)
        m = loadData("data/step/nohmestep_25_all_" + str(i) + ".txt")
        resNoHebbian01.append(m)
        m = loadData("data/step/mestep01_25_all_" + str(i) + ".txt")
        resNoHebbian20.append(m)
        m = loadData("data/step/mestep001_25_all_" + str(i) + ".txt")
        resNoHebbian40.append(m)

    mb, sb = avgData(base)
    mbh, sbh = avgData(baseh)
    mbh01, sbh01 = avgData(baseh01)
    mnh00,snh00 = avgData(resNoHebbian00)
    mnh10, snh10 = avgData(resNoHebbian10)
    mnh05, snh05 = avgData(resNoHebbian05)
    mnh75, snh75 = avgData(resNoHebbian75)
    mnh20, snh20 = avgData(resNoHebbian20)
    mnh40, snh40 = avgData(resNoHebbian40)
    mnh001, snh001 = avgData(resNoHebbian001)
    mnh01, snh01 = avgData(resNoHebbian01)

    cmap = plt.get_cmap("tab10")
    plt.axhline(mb[-1], color="k")
    plt.axhline(mbh[-1],linestyle="--", color="k")
    plt.axhline(mbh01[-1], linestyle=":", color="k")
    plt.plot(mnh01, color="b")
    plt.plot(mnh40,linestyle="--",color="b")
    plt.plot(mnh20, linestyle=":", color="b")

    plt.plot(mnh10, color="r")
    plt.plot(mnh75,linestyle="--", color="r")

    plt.plot(mnh00,  color="g")
    plt.plot(mnh05,linestyle="--", color="g")
    plt.plot(mnh001,linestyle=":", color="g")

    plt.plot([], linestyle="--", label="Hebbian $\eta$=0.01", color="gray")
    plt.plot([], linestyle=":", label="Hebbian $\eta$=0.1", color="gray")
    plt.plot([], label="MLP", color="gray")

    plt.plot([], label="Map Elites", color="b")
    plt.plot([], label="Step 0.5s", color="r")
    plt.plot([], label="Step 0.25s", color="g")

    plt.legend(loc="lower center", ncol=2)
    plt.savefig("plot/fitness.png", dpi =300)

    sers = list()
    for i in range(10):
        sers.append(getBestSer("data/step/step_50_final_"+str(i)+".txt"))
    with open("step_50.txt", "w") as f:
        f.write("x;y;best.serialized.robot\n")
        for i in range(10):
            x = i //5
            y = i % 5
            f.write(str(x)+";"+str(y)+";"+sers[i]+"\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
