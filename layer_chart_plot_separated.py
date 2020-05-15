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
        print("Directory ", dirName, " already exists")


def drawLine(layer, peerClassifcations, bezier, log_index=-1):
    for peerClassifcation in peerClassifcations:
        x = []
        y = []
        if (log_index == -1):
            for parsed_log in parsed_logs:
                datapoints = parsed_log[layer][peerClassifcation]
                for el in datapoints:
                    x.append(el["timestamp"])
                    y.append(el["nodeCount"])
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                x.append(el["timestamp"])
                y.append(el["nodeCount"])

        x = np.asarray(x)
        y = np.asarray(y)
        if (x.size == 0 or y.size == 0 or int(x.max()) == 0 or int(y.max()) == 0):
            return

        if (bezier == False):
            ax.plot(x, y)
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)
        else:
            verts = [(x[0], y[0])]
            codes = [Path.MOVETO]
            for i in range(1, x.size):
                verts.append((x[i], y[i]))
                codes.append(Path.CURVE4)

            path = Path(verts, codes)
            patch = mpatches.PathPatch(path, facecolor='none', lw=2)
            # ax.add_patch(patch)
            # ax.plot(x, y, 'x--', lw=2, color='black', ms=10)
            ax.plot(x, y, color=classesColors[peerClassifcation], label=peerClassifcation)
            ax.set_xlim(0, int(x.max()))
            ax.set_ylim(0, int(y.max()))
            print(verts)


for i in range(7):
    layers = parsed_logs[i].keys()
    for layer in layers:
        for _class in classes:
            print("Experiment " + str(i) + ", drawing " + layer + " " + _class + " line ")
            drawLine(layer, [_class], True, i)
            ax.set(xlabel='time (s)', ylabel='peer number', title="Experiment " + str(i) + ": " + layer + ', ' + _class)
            ax.grid()
            create_dir("output/2pc/experiment_" + str(i) + "/separated/")
            fig.savefig("output/2pc/experiment_" + str(i) + "/separated/" + layer.lower().replace(" ",
                                                                                                  "_") + "_" + _class.lower() + ".png")
            plt.show()
            fig, ax = plt.subplots()

        drawLine(layer, classes, False, i)
        ax.set(xlabel='time (s)', ylabel='peer number', title="Experiment " + str(i) + ": " + layer)
        ax.grid()
        # create_dir("output/2pc/experiment_" + str(i) + "/together/")
        # fig.savefig("output/2pc/experiment_" + str(i) + "/together/" + layer.lower().replace(" ","_") + ".png")
        plt.show()
        fig, ax = plt.subplots()