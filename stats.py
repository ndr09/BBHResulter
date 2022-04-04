from main import *
from MEdata import *
os.add_dll_directory(os.path.join(os.environ['JAVA_HOME'], 'bin', 'server'))
os.environ[
    'CLASSPATH'] = "C:\\Users\\opuse\\Desktop\\giorgia\\resulter\\jar\\vsr.jar"

import jnius_config

jnius_config.add_options('-Xrs', '-Xmx4096m')

from jnius import autoclass
import jnius



def getShape(ser):
    String = autoclass("java.lang.String")
    Pyworker = autoclass("it.units.erallab.Pyworker")

    return Pyworker.getShape(String(ser))



if __name__ == "__main__":
    data = {}
    bs = {}
    case = ["data/nohes_00","data/step/hstep01_00","data/es_00","data/step/step_25","data/step/h01step_25",
            "data/step/hstep_25", "data/step/nohmestep_25","data/step/nohme_10_step_25", "data/step/mestep01_25","data/step/me_10_step01_25",
            "data/step/mestep001_25", "data/step/me_10_step001_25"]
    conv = {
            "data/step/hstep_25":"ES\n$\eta$=0.01\nstep=0.25s",
            "data/step/step_25":"ES\nstep=0.25s",
            "data/step/hstep01_00":"ES\n$\eta$=0.1",
            "data/step/h01step_25":"ES\n$\eta$=0.1\nstep=0.25s",
            "data/es_00": "ES\n$\eta$=0.01",
            "data/nohes_00":"ES",
            "data/step/mestep01_25":"ME\n$\eta$=0.1\nstep=0.25s",
            "data/step/mestep001_25":"ME\n$\eta$=0.01\nstep=0.25s",
            "data/step/nohmestep_25":"ME\nstep=0.25s",
            "data/step/me_10_step01_25": "ME 10 \n$\eta$=0.1\nstep=0.25s",
            "data/step/me_10_step001_25": "ME 10 \n$\eta$=0.01\nstep=0.25s",
            "data/step/nohme_10_step_25": "ME 10 \nstep=0.25s"
            }

    for kind in case:
        data[conv[kind]] =list()
        bs[conv[kind]] = list()

    for kind in case:
        print(kind)
        for i in range(10):
            data[conv[kind]].append(getBestFitness(kind+"_all_"+str(i)+".txt"))

    dc = list()
    dk = list()
    for k, v in data.items():
        dc.append(v)
        dk.append(k)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.boxplot(dc, labels=dk)
    plt.ylabel("fitness $v_x$")
    plt.xticks(rotation=90)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    plt.savefig("plot/boxplot.png", dpi =300)

    for kind in case:
        print(conv[kind])
        for i in range(10):
            shape1 = getShape(getBestSer(kind+"_final_"+str(i)+".txt"))
            shape = np.full((len(shape1), len(shape1[0])), False)
            for i in range(len(shape1)):
                for j in range(len(shape1[i])):
                    if shape1[i][j]:
                        shape[i, j] = True
            shape = np.flip(shape.transpose(),0)
            print("\\vsr{" + str(len(shape[0])) + "}" + "{" + str(len(shape)) + "}" + str(shape).replace("\n",
                                                                                                         "").replace(
                "[[", "{").replace("[", "").replace("]]", "}").replace("]", "-").replace("True", "1").replace("False",
                                                                                                              "0").replace(
                " ", "").replace(",", ""))





