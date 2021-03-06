import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from scipy.ndimage import gaussian_filter1d
import numpy as np
import json
import math

colorMap = {
    'in': "green",
    'out': "red"
}

Path = mpath.Path

logs = os.listdir("./data/ip-port-in_out")
init_timestamp = 0

parsed_logs = []

for i in logs:
    if (i[0] == "_"):
        continue
    parsed_logs.append(json.load(open('./data/ip-port-in_out/' + i)))

fig, ax = plt.subplots()


def create_dir(dirName):
    try:
        os.makedirs(dirName)
    except FileExistsError:
        pass


create_dir("output/2pc/peer_churn_ip_port/")


def sortFirst(val):
    return val[0]


def fixTimestamp(timestamp):
    if (timestamp % 10 != 0):
        return (math.floor(timestamp / 10) * 10) - init_timestamp
    return timestamp - init_timestamp


def drawLine(log_index=-1, scatter=False):
    global init_timestamp
    highest_y = 0

    for type in ["in", "out"]:
        tuple_arr = []
        if (log_index == -1):
            # Evaluate all logs
            for parsed_log in parsed_logs:
                for timestamp, el in parsed_log.items():
                    if (init_timestamp == 0):
                        init_timestamp = fixTimestamp(int(timestamp))
                    tuple_arr.append((fixTimestamp(int(timestamp)), el[type + "_num"]))

                init_timestamp = 0

        else:
            datapoints = parsed_logs[log_index]
            for timestamp, el in datapoints.items():
                if (init_timestamp == 0):
                    init_timestamp = fixTimestamp(int(timestamp))
                tuple_arr.append((fixTimestamp(int(timestamp)), el[type + "_num"]))
            init_timestamp = 0

        if (len(tuple_arr) == 0):
            continue

        tuple_arr.sort(key=sortFirst)
        x, y = zip(*tuple_arr)
        x = np.asarray(x)
        y = np.asarray(y)
        # y = np.asarray(gaussian_filter1d(y_orig, 7))

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

        # ax.plot([0.75], [0.25], "ro")
        if (scatter):
            ax.scatter(x, y, s=1, color=colorMap[type], label=type)
        else:
            ax.plot(x, y, color=colorMap[type], label=type)

        ax.set_ylim(bottom=0, top=highest_y * 1.1)
        # ax.set_xlim(right=1600)

        print(len(verts))

        if (log_index != -1):
            try:
                os.remove("output/2pc/peer_churn_ip_port/experiment_" + str(log_index) + "_" + type + ".txt")
            except:
                pass
            txt_file = os.open("./output/2pc/peer_churn_ip_port/experiment_" + str(log_index) + "_" + type + ".txt",
                               os.O_RDWR | os.O_CREAT);
            for i in range(len(verts)):
                os.write(txt_file, bytes(
                    str(verts[i][0]) + " " + str(verts[i][1]) + "\n",
                    encoding="utf8"))  # works with any number of elements in a line
        else:
            try:
                os.remove("output/2pc/peer_churn_ip_port/experiment_all.txt")
            except:
                pass
            txt_file = os.open("./output/2pc/peer_churn_ip_port/experiment_all " + type + ".txt",
                               os.O_RDWR | os.O_CREAT);
            for i in range(len(verts)):
                os.write(txt_file, bytes(
                    str(verts[i][0]) + " " + str(verts[i][1]) + "\n",
                    encoding="utf8"))  # works with any number of elements in a line


for i in range(len(parsed_logs)):
    drawLine(i, True)
    ax.set(xlabel='Time (s)', ylabel='Peer number', title='Peer churn - Experiment ' + str(i))
    ax.grid()
    create_dir("output/2pc/peer_churn_ip_port/")
    plt.legend(loc="upper left")
    fig.savefig("output/2pc/peer_churn_ip_port/peer_churn_exp_" + str(i) + ".png", bbox_inches='tight')
    plt.show()
    fig, ax = plt.subplots()

drawLine(-1)
ax.set(xlabel='Time (s)', ylabel='Peer number', title='Peer churn - ALL Experiments Line')
ax.grid()
plt.legend(loc="upper left")
fig.savefig("output/2pc/peer_churn_ip_port/peer_churn_exp_all_line.png", bbox_inches='tight')
plt.show()
fig, ax = plt.subplots()

drawLine(-1, True)
ax.set(xlabel='Time (s)', ylabel='Peer number', title='Peer churn - ALL Experiments Scatter')
ax.grid()
plt.legend(loc="upper left")
fig.savefig("output/2pc/peer_churn_ip_port/peer_churn_exp_all_scatter.png", bbox_inches='tight')
plt.show()
fig, ax = plt.subplots()
