from main import *


def getMatrix(filename, size = 5):
    mat = np.full((size, size), -1.0)
    co = set()
    with open(filename, encoding='utf-8') as f:
        fr = csv.DictReader(f, delimiter=";")
        for l in fr:
            comp = float(l["individual→solution→shape→comp"])
            elon = float(l["individual→solution→shape→elon"])
            co.add(comp)
            fit = float(l["individual→fitness→velocity"])
            iy = int((comp-0.4) // 0.06) if comp <1.0 else 9
            ix = int(elon // 0.1)
            mat[iy, ix] = fit if fit >= mat[iy, ix] else mat[iy, ix]
    print(str(min(list(co)))+"   "+ str(max(list(co))))
    return mat


def avgMat(mats, size = 5):
    mat = np.zeros((size, size), dtype=float)
    count = np.zeros((size, size))
    for m in mats:
        for i in range(size):
            for j in range(size):
                if m[i, j] > -1:
                    mat[i, j] += m[i, j]
                    count[i, j] += 1


    for i in range(size):
        for j in range(size):
            mat[i, j] = mat[i, j] / count[i, j] if not count[i, j] == 0.0 else 0.0
    return mat, count


def maxMat(mats, size = 5):
    mat = np.zeros((size, size))
    for m in mats:
        for i in range(size):
            for j in range(size):
                if m[i, j] > mat[i, j]:
                    mat[i, j] = m[i, j]
    return mat


if __name__ == "__main__":
    ms = [list(), list(), list()]
    fig, axs = plt.subplots(3, 3)
    i = 0
    size = 10
    conv = {"me_10_step01": "$\eta$=0.1", "me_10_step001": "$\eta$=0.01", "nohme_10_step": "no hebbian"}
    for kind in ["me_10_step01", "me_10_step001", "nohme_10_step"]:
        for j in range(10):
            ms[i].append(getMatrix("data/step/" + kind + "_25_all_" + str(j) + ".txt", size))

        avg, count = avgMat(ms[i], size)
        maxm = maxMat(ms[i], size)

        ax = sns.heatmap(avg, ax=axs[i][0], vmin=0, vmax=15)

        ax.set_ylabel(conv[kind] + "\ncompactness")
        if i == 2:
            ax.set_xlabel("elongation")
        if i == 0:
            ax.set_title("Average")

        ax.invert_yaxis()
        ax = sns.heatmap(maxm, ax=axs[i][1],vmin=0, vmax=15)
        if i == 2:
            ax.set_xlabel("elongation")
        if i == 0:
            ax.set_title("max")
        ax.invert_yaxis()
        ax = sns.heatmap(count, ax=axs[i][2],vmin=0, vmax=10)
        if i == 2:
            ax.set_xlabel("elongation")
        if i == 0:
            ax.set_title("count")
        ax.invert_yaxis()
        print(kind + "  " + str(i))
        i += 1

    plt.subplots_adjust(wspace=0.5)
    plt.savefig("plot/map2.png", dpi=300)
