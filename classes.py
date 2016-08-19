import numpy as np
from matplotlib.mlab import PCA

class Node:
    def __init__(self, voxel, direction, score, region=None):
        self.region = region
        self.voxel = voxel
        self.direction = direction
        self.score = score



class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.regions = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_region(self, region):
        self.regions.append(region)

    def remove_region(self, region):
        self.regions.remove(region)


class Region:
    def __init__(self):
        self.nodes = []
        self.pca = None

    def add_node(self, node):
        self.nodes.append(node)

    def calc_pca(self):
        # print [node.voxel for node in self.nodes]
        self.pca = PCA(np.array([node.voxel for node in self.nodes], dtype=np.float))


