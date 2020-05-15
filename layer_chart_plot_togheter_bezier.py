import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import np
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
                        tuple_arr.append((el["timestamp"], el["nodeCount"]))
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                if el["timestamp"] > 1600:
                    continue
                tuple_arr.append((el["timestamp"], el["nodeCount"]))

        tuple_arr.sort(key=sortFirst)
        x,y = zip(*tuple_arr)
        x = np.asarray(x)
        y = np.asarray(y)

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
        patch = mpatches.PathPatch(path, facecolor='none', lw=1)
        ax.add_patch(patch)
        # ax.plot(x, y, 'x--', lw=2, color='black', ms=10)
        print(classesColors[peerClassifcation])
        # ax.plot([0.75], [0.25], "ro")
        # ax.plot(x, y, 'x', color=classesColors[peerClassifcation])
        ax.set_ylim(bottom=0, top=highest_y * 1.1)
        ax.set_xlim(right=1600)

        print(verts)



layers = set()
for parsed_log in parsed_logs:
    for k in parsed_log.keys():
        layers.add(k)

drawLine("Layer 1", ["Warm"], -1)
ax.set(xlabel='time (s)', ylabel='peer number', title="Bezier: Layer 1")
ax.grid()
create_dir("output/2pc/together_bezier/")
# fig.savefig("output/2pc/experiment_" + str(i) + "/together_bezier/" + layer.lower().replace(" ",
#                                                                                     "_") + ".png")
plt.show()
fig, ax = plt.subplots()

"""
for layer in layers:
    drawLine(layer, classes, -1)
    ax.set(xlabel='time (s)', ylabel='peer number', title="Bezier: " + layer)
    ax.grid()
    create_dir("output/2pc/together_bezier/")
    # fig.savefig("output/2pc/experiment_" + str(i) + "/together_bezier/" + layer.lower().replace(" ",
    #                                                                                     "_") + ".png")
    plt.show()
    fig, ax = plt.subplots()
"""