import numpy as np
#from matplotlib.mlab import PCA
from sklearn.decomposition import PCA

class Node:
    def __init__(self, voxel, direction, pca_dir, score, region=None):
        self.region = region
        self.voxel = voxel
        self.direction = direction
        self.score = score
        self.pca_dir = pca_dir


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
        self.pc = PCA(n_components=3)
        self.nodes = []
        self.pca = None
        self.eigenvalues = None
        self.id = 0

    def add_node(self, node):
        self.nodes.append(node)

    def calc_pca(self):
        # print [node.voxel for node in self.nodes]
        self.pca = self.pc.fit(np.array([node.voxel for node in self.nodes], dtype=np.float))
        self.eigenvalues = self.pca.explained_variance_

    @staticmethod
    def connect(region_1, region_2):
        unified_region = Region()
        unified_region.nodes = region_1.nodes + region_2.nodes
        if len(unified_region.nodes) > 8:
            try:
                unified_region.calc_pca()
            except Exception as e:
                print "pca problem"
        for node in unified_region.nodes:
            node.region = unified_region
        return unified_region


