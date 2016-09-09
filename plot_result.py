"""
3D graph plot, showing the resulted regions, in different colors.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # DO NOT REMOVE THIS LINE. This allows to plot when in GUI mode
import numpy as np


def main(graph, target_size):
    plt.clf()
    fig = plt.figure(figsize=(30, 30))

    ax = fig.add_subplot(111, projection='3d')

    colors = []
    points = []
    color = float(0)
    for region in graph.regions:
        for node in region.nodes:
            points.append(node.voxel)
        colors = np.concatenate((colors, np.array([color for k in range(len(region.nodes))], dtype=np.float)), axis=0)
        color = (color + 0.07) % 1

    x_all = np.array([])
    y_all = np.array([])
    z_all = np.array([])

    c_all = np.array([])
    s_all = np.array([])
    x = np.array([x[0] for x in points], \
                 dtype=np.float)
    y = np.array([y[1] for y in points], \
                 dtype=np.float)
    z = np.array([z[2] for z in points], \
                 dtype=np.float)
    c = np.array(colors, dtype=np.float)

    x_all = np.concatenate((x_all, x), axis=0)
    y_all = np.concatenate((y_all, y), axis=0)
    z_all = np.concatenate((z_all, z), axis=0)

    c_all = c

    plt.tick_params(axis='both', which='major', labelsize=55)

    ax.scatter(x_all, y_all, z_all, c=c_all, alpha=0.5)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
