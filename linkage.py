import numpy as np

from classes import *
from graph import angle, connect
import math
from scipy.spatial import distance


ANGLE_BETWEEN_REGIONS = math.pi / 9
MID_DIST_DEFAULT = 10
LINE_DIST_DEFAULT = 10


def helix_radius_satisfible(region):
    pca = region.calc_pca()
    lambda1, lambda2 = pca
    return math.sqrt(lambda1) <= 3.5 and math.sqrt(lambda2) <= 3.5


def angle_satisfiable(region_1, region_2):
    angle_1, angle_2 = region_1.calc_pca().Wt[0], region_2.calc_pca().Wt[0]
    return angle(angle_1, angle_2) < ANGLE_BETWEEN_REGIONS


def midpoint_distance(region_1, region_2):
    mean_1 = np.array(region_1.nodes).mean()
    mean_2 = np.array(region_2.nodes).mean()
    return distance_between_points(mean_1, mean_2)


def line_distance(region_1, region_2):
    min_dist = float('Inf')

    for node_1 in region_1:
        for node_2 in region_2:
            dist = distance_between_points(node_1, node_2)
            if dist < min_dist:
                min_dist = dist
    return min_dist


def distances_satisfaible(region_1, region_2):
    return midpoint_distance(region_1, region_2) < MID_DIST_DEFAULT and line_distance(region_1, region_2) < LINE_DIST_DEFAULT


def distance_between_points(point_1, point_2):
    dist = numpy.linalg.norm(point_1 - point_2)


def link_regions(graph):

    for region_1 in graph.regions:
        for region_2 in graph.regions:
            if region_1 != region_2:
                linked_region = Region()
                linked_region.nodes = region_1 + region_2.nodes
                if helix_radius_satisfible(linked_region) \
                    and angle_satisfiable(region_1, region_2) \
                    and distances_satisfaible(region_1, region_2):
                    connect(region_1.nodes[0], region_2.nodes[0])

