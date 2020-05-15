import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import medfilt
import numpy as np
import json

Path = mpath.Path
classes = ["Freerider", "Cold", "Warm", "Hot"]
classesColors = {
    'Freerider': "black",
    'Cold': "blue",
    'Warm': "green",
    'Hot': "red"
}

layerColors = {
    'Layer 1': "red",
    'Layer 2': "green",
    'Layer 3': "blue",
    'Layer 4': "black",
    'Layer 5': "cyan"
}

layersMarkers = {
    'Layer 1': "x",
    'Layer 2': "D",
    'Layer 3': "o",
    'Layer 4': "^",
    'Layer 5': "v"
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


def drawClassificationChart(layers, peerClassifcation, log_index=-1):
    highest_y = 0

    for layer in layers:
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
                        tuple_arr.append((el["timestamp"], el["nodeCount"]))
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                if el["timestamp"] > 1600:
                    continue
                tuple_arr.append((el["timestamp"], el["nodeCount"]))

        if (len(tuple_arr) == 0):
            continue

        tuple_arr.sort(key=sortFirst)
        x, y = zip(*tuple_arr)
        x = np.asarray(x)
        y = np.asarray(gaussian_filter1d(y, 7))

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

        path = Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor='none', lw=2)
        # ax.add_patch(patch)
        # ax.plot(x, y, 'x--', lw=2, color='black', ms=10)
        print(layerColors[layer])
        # ax.plot([0.75], [0.25], "ro")
        marker_style = dict(marker=layersMarkers[layer], markersize=5, markerfacecoloralt='white', fillstyle='full', markevery=0.05)
        ax.plot(x, y, color=classesColors[peerClassifcation], label=layer, lw=1, **marker_style)
        ax.set_ylim(bottom=0, top=highest_y * 1.1)
        ax.set_xlim(right=1600)

        print(verts)


layers = set()
for parsed_log in parsed_logs:
    for k in parsed_log.keys():
        layers.add(k)
layers = ["Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5"]


# plt.show()

for type in classesColors.keys():
    drawClassificationChart(layers, type, -1)
    ax.set(xlabel='time (s)', ylabel='peer number', title=type)
    ax.grid()
    create_dir("output/2pc/layer_together_gaussian_same_color/")
    plt.legend(loc="upper left")
    fig.savefig("output/2pc/layer_together_gaussian_same_color/" + type.lower().replace(" ", "_") + ".png")
    plt.show()
    fig, ax = plt.subplots()
