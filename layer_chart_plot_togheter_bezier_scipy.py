import matplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import np
import numpy as np
import json
from scipy.special import comb

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
    parsed_logs.append(json.load(open('./data/2pc/' + i)))

fig, ax = plt.subplots()

def create_dir(dirName):
    try:
        os.makedirs(dirName)
    except FileExistsError:
        pass

def sortFirst(val):
    return val[0]

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i



def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.
       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000
        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals



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
                        tuple_arr.append((el["timestamp"], el["nodeCount"]))
        else:
            datapoints = parsed_logs[log_index][layer][peerClassifcation]
            for el in datapoints:
                tuple_arr.append((el["timestamp"], el["nodeCount"]))

        tuple_arr.sort(key=sortFirst)
        x, y = zip(*tuple_arr)
        x = np.asarray(x)
        y = np.asarray(y)

        if (x.size == 0 or y.size == 0 or int(x.max()) == 0 or int(y.max()) == 0):
            continue

        if (int(y.max()) > highest_y):
            highest_y = int(y.max())

        xvals, yvals = bezier_curve(tuple_arr, nTimes=1)
        plt.plot(xvals, yvals)
        plt.plot(x, y, "r")
        for nr in range(len(tuple_arr)):
            plt.text(tuple_arr[nr][0], tuple_arr[nr][1], nr)
        ax.set_ylim(bottom=0, top=highest_y * 1.1)



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