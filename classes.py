"""
Holds the various classes and data structures.
Used by the algorithm graphs creation and manipulation
"""

import numpy as np
from sklearn.decomposition import PCA

class Node:
    """
    Description
    ----------
    Node in the regional graph

    Attributes
    ----------
    region: Region. Points to the region to which the node belongs to.
    voxel: list. x,y,z coordinates in the fullmap matrix.
    direction: tuple. The node's assigned region.
    score: float. The direction correlation score.
    pca_dir: float. pc1 direction of the Node.
    """
    def __init__(self, voxel, direction, pca_dir, score, region=None):
        self.region = region
        self.voxel = voxel
        self.direction = direction
        self.score = score
        self.pca_dir = pca_dir


class Graph:
    """
    Description
    ----------
    Graph with regions, nodes and edges between nodes

    Attributes
    ----------
    nodes: list. The graph's nodes.
    edges: list. The graphs edges
    regions: list. The graphs regions
    """
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
    """
    Description
    ----------
    Graph with regions, nodes and edges between nodes

    Attributes
    ----------
    pc: static instance for pca calculations
    nodes: list. The graphs edges
    pca: PCA. The region's pca data structure with eigenvectors
    eigenvalues: list. The region's eigenvalues
    id: int. The region's identification number
    """
    def __init__(self):
        self.pc = PCA(n_components=3)
        self.nodes = []
        self.pca = None
        self.eigenvalues = None
        self.id = 0

    def add_node(self, node):
        self.nodes.append(node)

    def calc_pca(self):
        # update the principle components (eigenvalues and eigenvectores of the region
        self.pca = self.pc.fit(np.array([node.voxel for node in self.nodes], dtype=np.float))
        self.eigenvalues = self.pca.explained_variance_

    @staticmethod
    def connect(region_1, region_2):
        """
        Connect between two regions
        :param region_1:
        :param region_2:
        :return: The unified region
        """
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


