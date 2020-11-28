import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import np
from scipy.ndimage import gaussian_filter1d
import numpy as np
import json
import math

Path = mpath.Path
classes = ["Freerider", "Cold", "Warm", "Hot"]
classesColors = {
    'Freerider': "black",
    'Cold': "blue",
    'Warm': "green",
    'Hot': "red"
}

_2pclogs = os.listdir("./data/2pc")
parsed_logs = []

for i in _2pclogs:
    if(i[0] == "_"):
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
    if (timestamp % 10 != 0):
        return math.floor(timestamp / 10) * 10
    return timestamp

def drawLine(layer, peerClassifcations, log_index=-1):
    highest_y = 0
    for peerClassifcation in peerClassifcations:
        x = []
        y = []
        tuple_arr = []
        if (log_index == -1):
            for parsed_log in parsed_logs:
                if layer in parsed_log:
                    datapoints = parsed_log[layer][peerClassifcation]
                    for el in datapoints:
                        if el["timestamp"] > 1600:
                            continue
                        tuple_arr.append((fixTimestamp(el["timestamp"]), el["nodeCount"]))
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                if el["timestamp"] > 1600:
                    continue
                tuple_arr.append((fixTimestamp(el["timestamp"]), el["nodeCount"]))

        if(len(tuple_arr) == 0):
            continue

        tuple_arr.sort(key=sortFirst)
        x,y = zip(*tuple_arr)
        x = np.asarray(x)
        y_orig = np.asarray(y)
        y = np.asarray(gaussian_filter1d(y_orig, 7))

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
        ax.plot(x, y, color=classesColors[peerClassifcation], label=peerClassifcation)
        ax.set_ylim(bottom=0, top=highest_y * 1.1)
        ax.set_xlim(right=1600)

        print(verts)



layers = set()
for parsed_log in parsed_logs:
    for k in parsed_log.keys():
        layers.add(k)

"""
drawLine("Layer 1", ["Warm"], -1)
ax.set(xlabel='time (s)', ylabel='peer number', title="Layer 1")
ax.grid()
create_dir("output/2pc/together_gaussian/")

plt.show()
fig, ax = plt.subplots()
"""

for layer in layers:
    drawLine(layer, classes, -1)
    ax.set(xlabel='time (s)', ylabel='peer number', title=layer)
    ax.grid()
    create_dir("output/2pc/together_gaussian/")
    if layer == "Layer 1" or layer == "Layer 4" or layer == "Layer 6" or layer == "Layer 5" or layer == "Unconnected nodes":
        plt.legend(loc="upper right")
    else:
        plt.legend(loc="upper left")
    fig.savefig("output/2pc/together_gaussian/" + layer.lower().replace(" ", "_") + ".png")
    plt.show()
    fig, ax = plt.subplots()