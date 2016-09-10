"""
Connect graph regions under regional restrictions.
"""
import math

import utils
from classes import *
from graph import angle
from messages import Messages
from scipy.spatial import distance


ANGLE_BETWEEN_REGIONS = 20

def helix_radius_satisfiable(region, APIX):
    """
    Check if region's eigenvalues match a helix shape
    :param region: Region
    :return: boolean
    """
    region.calc_pca()
    # Get pc2 and pc3 (region radius values) and check their length cond.
    lambda2, lambda3 = region.eigenvalues[1], region.eigenvalues[2]
    return math.sqrt(lambda2) <= 3.5/APIX and math.sqrt(lambda3) <= 3.5/APIX


def angle_satisfiable(region_1, region_2):
    """
    Check if the angle between the main vectors of both regions is below predefined thresh.
    :param region_1: Region
    :param region_2: Region
    :return: float
    """
    try:
        region_1.calc_pca()
        region_2.calc_pca()
    except Exception as e:
        print len(region_1.nodes), len(region_2.nodes)
        return False
    angle_1, angle_2 = region_1.pca.components_[0], region_2.pca.components_[0]
    return angle(angle_1, angle_2)*57.2958 < ANGLE_BETWEEN_REGIONS


def midpoint_distance(region_1, region_2):
    """
    Get the midpoint dist. between two regions
    :param region_1: Region
    :param region_2: Region
    :return: float
    """
    # The midpoint dist. is calculated as the dist. between both regions center points
    return distance_between_points(region_1.pca.mean_, region_2.pca.mean_)


def line_distance(region_1, region_2):
    """
    Get the line dist. between two regions
    :param region_1: Region
    :param region_2: Region
    :return: float
    """
    return distance.cdist([node.voxel for node in region_1.nodes], [node.voxel for node in region_2.nodes], metric="euclidean").min()

def distances_satisfiable(region_1, region_2, mid, line, APIX):
    """
    Check if both line and midpoint dist. are below predefined thesh.
    :param region_1: Region
    :param region_2: Region
    :return: boolean
    """
    return midpoint_distance(region_1, region_2) < mid/APIX and line_distance(region_1, region_2) < line/APIX


def distance_between_points(point_1, point_2):
    """
    Get the distance between two point voxels
    """
    return distance.euclidean(point_1, point_2)


def main(graph, mid, line, apix):
    """
    :param graph: regional graph
    :param mid: midpoint dist. thresh.
    :param line: line dist. thresh.
    :return: regional graph after linking its regions
    """

    graph.regions = [region for region in graph.regions if len(region.nodes) >= 8]

    paired_regions = True # Boolean that tell us if we should run the main linking loops again
    last_unified = 0 # Lest unified i index
    while paired_regions:
        paired_regions = False
        start_over = False # Second boolean for loop breaking

        # Run loop from first region to the last unified and try to unify with the last appended
        for i in range(0, last_unified):

            region_1 = graph.regions[i]
            last_region = graph.regions[len(graph.regions)-1]

            # If the angle and dist. restrictions are not satisfied, continue to the next region
            if not (angle_satisfiable(region_1, last_region) and distances_satisfiable(region_1, last_region, mid, line, apix)):
                continue

            # Otherwise, link the regions and test radius restriction
            linked_region = Region.connect(region_1, last_region)
            if helix_radius_satisfiable(linked_region, apix):
                # If all valid, regions should link and loop should start over from first region
                paired_regions = True
                graph.regions.remove(region_1)
                graph.regions.remove(last_region)
                graph.regions.append(linked_region)
            utils.set_status(Messages.START_LINK, same_line=True, effect=True)
        # If no regions connected with the new regions from last loop, run from the last unified region index
        for i in range(last_unified, len(graph.regions)):
            for j in range(i + 1, len(graph.regions)):

                region_1 = graph.regions[i]
                region_2 = graph.regions[j]

                # If the angle and dist. restrictions are not satisfied, continue to the next region
                if not (angle_satisfiable(region_1, region_2) and distances_satisfiable(region_1, region_2, mid, line, apix)):
                    continue

                # Otherwise, link the regions and test radius restriction
                linked_region = Region.connect(region_1, region_2)
                if helix_radius_satisfiable(linked_region, apix):
                    # If all valid, regions should link and loop should start over from first region
                    paired_regions = True
                    graph.regions.remove(region_1)
                    graph.regions.remove(region_2)
                    graph.regions.append(linked_region)
                    # Start over from first region, graph.regions changed
                    start_over = True
                    break

            if start_over:
                # save to which index we have arrived last time we linked region1 with a non-last region2
                last_unified = i
                break
            utils.set_status(Messages.START_LINK, same_line=True, effect=True)

    return graph