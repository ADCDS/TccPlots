import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from scipy.ndimage import gaussian_filter1d
import numpy as np
import json
import math
import shutil

Path = mpath.Path
classes = ["Freerider", "Cold", "Warm", "Hot"]
classesColors = {
    'Freerider': "black",
    'Cold': "blue",
    'Warm': "green",
    'Hot': "red"
}
classesMarkers = {
    'Freerider': '',
    'Cold': "s",
    'Warm': "x",
    'Hot': "o"
}

_2pclogs = os.listdir("./data/2pc")
parsed_logs = []

for i in _2pclogs:
    if (i[0] == "_"):
        continue
    parsed_logs.append(json.load(open('./data/2pc/' + i)))

fig, ax = plt.subplots()


def create_dir(dirName):
    try:
        os.makedirs(dirName)
    except FileExistsError:
        pass


def sortFirst(val):
    return val[0]


def fixTimestamp(timestamp):
    # if (timestamp % 10 != 0):
    #     return math.floor(timestamp / 10) * 10
    return timestamp


def howManyAt(peerClassifcation, time, log_index=-1):
    if (log_index == -1):
        raise ValueError('not implemented yet')
    else:
        ret = 0
        for layer in layers:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            found = False
            for el in datapoints:
                if el["timestamp"] == time:
                    ret += el["nodeCount"]
                    found = True
            # if(found == False):
            # raise ValueError('no time ' + str(time))
        return ret


def percentageOf(numberOfNodes, peerClassifcation, time, log_index=-1):
    total = howManyAt(peerClassifcation, time, log_index)
    if (total == 0):
        return 0
    return numberOfNodes * 100 / total


def printVerts(layer, className, verts):
    create_dir("output/2pc/together_gaussian_pct/2pc_sbrc/pct/" + layer)
    f = open("output/2pc/together_gaussian_pct/2pc_sbrc/pct/" + layer + "/" + className + ".txt", "a")
    for x in verts:
        print(x)
        f.write(str(x[0]) + " " + str(x[1]) + "\n")
    f.close()


def drawLinePct(layer, peerClassifcations, log_index=-1):
    highest_y = 0
    for peerClassifcation in peerClassifcations:
        x = []
        y = []
        tuple_arr = []
        if (log_index == -1):
            for idx, parsed_log in enumerate(parsed_logs):
                if layer in parsed_log:
                    datapoints = parsed_log[layer][peerClassifcation]
                    for el in datapoints:
                        # if el["timestamp"] > 1600:
                        #     continue
                        # tuple_arr.append((fixTimestamp(el["timestamp"]), el["nodeCount"]))
                        tuple_arr.append((fixTimestamp(el["timestamp"]),
                                          percentageOf(el["nodeCount"], peerClassifcation, el["timestamp"], idx)))
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                # if el["timestamp"] > 1600:
                #     continue
                tuple_arr.append((fixTimestamp(el["timestamp"]),
                                  percentageOf(el["nodeCount"], peerClassifcation, el["timestamp"], log_index)))
                # print("->at " + str(el["timestamp"]) + "s there is " + str(howManyAt("Hot", el["timestamp"], log_index)) + " " + peerClassifcation + " in the network")
                # print("->at " + str(el["timestamp"]) + "s there is " + str(el["nodeCount"]) + " ("+str(percentageOf(el["nodeCount"], peerClassifcation, el["timestamp"], log_index))+") " + peerClassifcation + " in " + layer + "\n")

        if (len(tuple_arr) == 0):
            continue

        tuple_arr.sort(key=sortFirst)
        x, y = zip(*tuple_arr)
        x = np.asarray(x)
        y_orig = np.asarray(y)
        # y = y_orig
        y = np.asarray(gaussian_filter1d(y_orig, 7))
        printVerts(layer, peerClassifcation, tuple_arr)

        if (x.size == 0 or y.size == 0 or int(x.max()) == 0 or int(y.max()) == 0):
            continue

        if (int(y.max()) > highest_y):
            highest_y = int(y.max())

        verts = [(x[0], y[0])]
        codes = [Path.MOVETO]
        for i in range(1, x.size):
            verts.append((x[i], y[i]))
            codes.append(Path.CURVE4)
        codes[len(codes) - 1] = Path.STOP

        # path = Path(verts, codes)
        # patch = mpatches.PathPatch(path, facecolor='none', lw=2)
        # ax.add_patch(patch)
        # ax.plot(x, y, 'x', lw=1, color=classesColors[peerClassifcation])
        print(classesColors[peerClassifcation])
        # ax.plot([0.75], [0.25], "ro")
        # ax.scatter(x, y_orig, color=classesColors[peerClassifcation], s=1)
        newLabel = peerClassifcation
        if (newLabel == "Freerider"):
            newLabel = "Free Rider"
        # mec="black"
        fillstyle = "none"
        if (peerClassifcation == "Hot"):
            fillstyle = "full"
        ax.plot(x, y, color=classesColors[peerClassifcation], label=newLabel, marker=classesMarkers[peerClassifcation],
                markevery=.1, fillstyle=fillstyle)

        ax.set_ylim(bottom=0, top=100)
        # ax.set_xlim(right=1600)

        print(verts)


"""layers = set()
for parsed_log in parsed_logs:
    for k in parsed_log.keys():
        layers.add(k)
"""
layers = ["Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5", "Layer 6"]
"""
drawLinePct("Layer 1", ["Warm", "Hot"], 1)
ax.set(xlabel='time (s)', ylabel='peer number', title="Layer 1")
ax.grid()
create_dir("output/2pc/together_gaussian/")

plt.show()
fig, ax = plt.subplots()
"""

try:
    shutil.rmtree("output/2pc/together_gaussian_pct/2pc_sbrc/pct/")
except:
    print("")

for layer in layers:
    drawLinePct(layer, classes, -1)

    if (layer == "Unconnected nodes"):
        # ax.set(xlabel='tempo (s)', ylabel='Número de peers', title="Número de peers desconectados por tempo")
        ax.set(xlabel='Time (s)', ylabel='Percentage of disconnected peers per class', title='k=1 - ' + layer)
    else:
        # ax.set(xlabel='tempo (s)', ylabel='Número de peers', title=layer)
        ax.set(xlabel='Time (s)', ylabel='Percentage of peers per class', title='k=1 - ' + layer)

    ax.grid()
    create_dir("output/2pc/together_gaussian_pct/2pc_sbrc/")
    create_dir("output/2pc/together_gaussian_pct/2pc_sbrc/data/")
    if layer == "Layer 1" or layer == "Layer 4" or layer == "Layer 6" or layer == "Layer 5" or layer == "Unconnected nodes":
        plt.legend(loc="upper right")
    else:
        plt.legend(loc="upper left")
    fig.savefig("output/2pc/together_gaussian_pct/2pc_sbrc/" + layer.lower().replace(" ", "_") + ".png")
    plt.show()
    fig, ax = plt.subplots()

    # for idx, parsed_log in enumerate(parsed_logs):
    #     drawLinePct(layer, classes, idx)
    #
    #     if (layer == "Unconnected nodes"):
    #         # ax.set(xlabel='tempo (s)', ylabel='Número de peers', title="Número de peers desconectados por tempo")
    #         ax.set(xlabel='tempo (s)', ylabel='Número de peers desconectados', title=layer)
    #     else:
    #         # ax.set(xlabel='tempo (s)', ylabel='Número de peers', title=layer)
    #         ax.set(xlabel='tempo (s)', ylabel='Número de peers', title=layer)
    #
    #     ax.grid()
    #     create_dir("output/2pc/experiment_"+str(idx)+"_pct/")
    #     if layer == "Layer 1" or layer == "Layer 4" or layer == "Layer 6" or layer == "Layer 5" or layer == "Unconnected nodes":
    #         plt.legend(loc="upper right")
    #     else:
    #         plt.legend(loc="upper left")
    #     fig.savefig("output/2pc/experiment_"+str(idx)+"_pct/" + layer.lower().replace(" ", "_") + ".png")
    #     plt.show()
    #     fig, ax = plt.subplots()
    #     break
