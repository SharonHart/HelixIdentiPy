import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

def plot_matrix(graph, target_size):
    plot = np.zeros(target_size)
    for region in graph.regions:
        for node in region.nodes:
            x, y, z = node.voxel
            plot[x, y, z] = 1

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    X, Y = np.mgrid[:target_size[0], :target_size[1]]

    surf = ax.plot_surface(X,Y, plot)
    plt.show()
