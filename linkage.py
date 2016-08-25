import numpy as np

from classes import *
from graph import angle, connect_regions
import math
from scipy.spatial import distance


ANGLE_BETWEEN_REGIONS = math.pi / 9
MID_DIST_DEFAULT = 10
LINE_DIST_DEFAULT = 10


def helix_radius_satisfible(region):
    pca = region.calc_pca()
    lambda1, lambda2 = region.pca.s[1], region.pca.s[2]
    return math.sqrt(lambda1) <= 3.5 and math.sqrt(lambda2) <= 3.5


def angle_satisfiable(region_1, region_2):
    try:
        region_1.calc_pca()
        region_2.calc_pca()
    except Exception as e:
        print len(region_1.nodes), len(region_2.nodes)
        return False
    angle_1, angle_2 = region_1.pca.Wt[0], region_2.pca.Wt[0]
    return angle(angle_1, angle_2) < ANGLE_BETWEEN_REGIONS


def midpoint_distance(region_1, region_2):
    mean_1 = np.array([node.voxel for node in region_1.nodes]).mean()
    mean_2 = np.array([node.voxel for node in region_2.nodes]).mean()
    return distance_between_points(mean_1, mean_2)


def line_distance(region_1, region_2):
    min_dist = float('Inf')

    for node_1 in region_1.nodes:
        for node_2 in region_2.nodes:
            dist = distance_between_points(node_1.voxel, node_2.voxel)
            if dist < min_dist:
                min_dist = dist
    return min_dist


def distances_satisfaible(region_1, region_2):
    return midpoint_distance(region_1, region_2) < MID_DIST_DEFAULT and line_distance(region_1, region_2) < LINE_DIST_DEFAULT


def distance_between_points(point_1, point_2):
    dist = np.linalg.norm(np.array(point_1) - np.array(point_2))


def link_regions(graph):
    graph.regions = [region for region in graph.regions if len(region.nodes) >= 8]
    continue_scanning = True
    while continue_scanning:
        regionsss = graph.regions[:]
        to_remove = []
        to_add = []
        keep_it = False
        for i in range(len(graph.regions)):
            for j in range(i+1, len(graph.regions)):
                linked_region = Region()
                region_1 = regionsss[i]
                region_2 = regionsss[j]
                linked_region.nodes = region_1.nodes + region_2.nodes
                if helix_radius_satisfible(linked_region) \
                        and angle_satisfiable(region_1, region_2) \
                        and distances_satisfaible(region_1, region_2):
                    to_remove.append(region_1)
                    to_remove.append(region_2)
                    to_add.append(connect_regions(region_1.nodes[0], region_2.nodes[0])
)
                    keep_it = True
        if not keep_it: continue_scanning = False
        for r in to_remove:
            graph.remove_region(r)
        for r in to_add:
            graph.regions.append(r)
    return graph
                # for region_1 in graph.regions:
    #     for region_2 in graph.regions:
    #         if region_1 != region_2:

