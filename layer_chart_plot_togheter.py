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


def drawLine(layer, peerClassifcations, log_index=-1):
    highest_y = 0
    for peerClassifcation in peerClassifcations:
        x = []
        y = []

        if (log_index == -1):
            for parsed_log in parsed_logs:
                datapoints = parsed_log[layer][peerClassifcation]
                for el in datapoints:
                    if el["timestamp"] > 1600:
                        continue

                    x.append(el["timestamp"])
                    y.append(el["nodeCount"])
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                if el["timestamp"] > 1600:
                    continue

                x.append(el["timestamp"])
                y.append(el["nodeCount"])

        x = np.asarray(x)
        y = np.asarray(y)

        if (x.size == 0 or y.size == 0 or int(x.max()) == 0 or int(y.max()) == 0):
            continue

        if (int(y.max()) > highest_y):
            highest_y = int(y.max())
        ax.plot(x, y, color=classesColors[peerClassifcation], label=peerClassifcation)
        ax.set_ylim(bottom=0, top=highest_y * 1.1)
        ax.set_xlim(right=1600)



for i in range(7):
    layers = parsed_logs[i].keys()
    for layer in layers:
        drawLine(layer, classes, i)
        ax.set(xlabel='time (s)', ylabel='peer number', title="Experiment " + str(i) + ": " + layer)
        ax.grid()
        create_dir("output/2pc/experiment_" + str(i) + "/together/")
        fig.savefig("output/2pc/experiment_" + str(i) + "/together/" + layer.lower().replace(" ",
                                                                                             "_") + ".png")
        plt.show()
        fig, ax = plt.subplots()
