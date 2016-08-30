import matplotlib.pyplot as plt

import numpy as np

"""
2d picture, not very informative
"""


def plot_matrix2(graph, target_size):
    plt.clf()
    out_file_name = "./rainbow_pic" + ".png"

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
    # s = np.array([50 for k in range(len(x))], dtype=np.float)

    x_all = np.concatenate((x_all, x), axis=0)
    y_all = np.concatenate((y_all, y), axis=0)
    z_all = np.concatenate((z_all, z), axis=0)

    c_all = c
    # s_all = np.concatenate((s_all, s), axis=0)

    plt.figure(figsize=(30, 30))
    plt.tick_params(axis='both', which='major', labelsize=55)

    plt.scatter(x_all, y_all, c=c_all, alpha=0.5)
    # plt.xlim(X_LIM)
    # plt.ylim(Y_LIM)

    plt.savefig(out_file_name)

    plt.clf()
    plt.close()

    x_allr = np.array([])
    y_allr = np.array([])
    c_allr = np.array([])
    s_allr = np.array([])
    x_allg = np.array([])
    y_allg = np.array([])
    c_allg = np.array([])
    s_allg = np.array([])

    plt.figure(figsize=(30, 30))
    plt.show()


"""
3d picture of resulted regions and their nodes
"""


def plot_matrix(graph, target_size):
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
    # s = np.array([50 for k in range(len(x))], dtype=np.float)

    x_all = np.concatenate((x_all, x), axis=0)
    y_all = np.concatenate((y_all, y), axis=0)
    z_all = np.concatenate((z_all, z), axis=0)

    c_all = c
    # s_all = np.concatenate((s_all, s), axis=0)

    plt.tick_params(axis='both', which='major', labelsize=55)

    ax.scatter(x_all, y_all, z_all, c=c_all, alpha=0.5)
    # plt.xlim(X_LIM)
    # plt.ylim(Y_LIM)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    # plt.savefig("3d_plot.png")
    plt.show()
    # plt.savefig(out_file_name)
    #
    # plt.clf()
    # plt.close()


    # plt.figure(figsize=(30, 30))
    # plt.show()
