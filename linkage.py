import numpy as np
import copy
from classes import *
from graph import angle
import math
from scipy.spatial import distance


ANGLE_BETWEEN_REGIONS = math.pi / 9
MID_DIST_DEFAULT = 100000000000
LINE_DIST_DEFAULT = 10

APIX = None

def helix_radius_satisfible(region):
    region.calc_pca()
    lambda1, lambda2 = region.eigenvalues[1], region.eigenvalues[2]
    return math.sqrt(lambda1) <= 3.5/APIX and math.sqrt(lambda2) <= 3.5/APIX


def angle_satisfiable(region_1, region_2):
    try:
        region_1.calc_pca()
        region_2.calc_pca()
    except Exception as e:
        print len(region_1.nodes), len(region_2.nodes)
        return False
    angle_1, angle_2 = region_1.pca.components_[0], region_2.pca.components_[0]
    return angle(angle_1, angle_2) < ANGLE_BETWEEN_REGIONS


def midpoint_distance(region_1, region_2):
    return distance_between_points(region_1.pca.mean_, region_2.pca.mean_)


def line_distance(region_1, region_2):
    min_dist = float('Inf')

    for node_1 in region_1.nodes:
        for node_2 in region_2.nodes:
            dist = distance_between_points(np.array(node_1.voxel), np.array(node_2.voxel))
            if dist < min_dist:
                min_dist = dist
    return min_dist


def distances_satisfaible(region_1, region_2):
    return midpoint_distance(region_1, region_2) < MID_DIST_DEFAULT/APIX and line_distance(region_1, region_2) < LINE_DIST_DEFAULT/APIX


def distance_between_points(point_1, point_2):
    return np.linalg.norm(point_1 - point_2)


def link_regions(graph, apix):
    global APIX
    APIX = apix
    graph.regions = [region for region in graph.regions if len(region.nodes) >= 8]
    paired_regions = True
    last_unified = 0
    while paired_regions:
        paired_regions = False
        start_over = False

        for i in range(0, last_unified):
            print i, len(graph.regions)-1, len(graph.regions)
            region_1 = graph.regions[i]
            last_region = graph.regions[len(graph.regions)-1]
            if not (angle_satisfiable(region_1, last_region) and distances_satisfaible(region_1, last_region)):
                continue
            linked_region = Region.connect(region_1, last_region)
            if helix_radius_satisfible(linked_region):
                paired_regions = True
                graph.regions.remove(region_1)
                graph.regions.remove(last_region)
                graph.regions.append(linked_region)

        for i in range(last_unified, len(graph.regions)):
            for j in range(i + 1, len(graph.regions)):
                print i,j, len(graph.regions)

                region_1 = graph.regions[i]
                region_2 = graph.regions[j]
                if not (angle_satisfiable(region_1, region_2) and distances_satisfaible(region_1, region_2)):
                    continue
                linked_region = Region.connect(region_1, region_2)
                if helix_radius_satisfible(linked_region):
                    paired_regions = True
                    graph.regions.remove(region_1)
                    graph.regions.remove(region_2)
                    graph.regions.append(linked_region)
                    start_over = True
                    break
            if start_over:
                last_unified = i
                break
    return graph