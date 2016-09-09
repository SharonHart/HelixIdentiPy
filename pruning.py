"""
Prune the resulted regions, removing non-alpha-helical resembling regions.
Returns the final matrix.
A cell with value 0 was found to be non-helix, otherwise, we assign 1-N id for each region and a cell assigned to it.
"""
import numpy as np
import math

STD_THRESHOLD = 0.2
HELIX_LENGTH_THRESHOLD = 10000

def main(graph, target_map):
    # calculate non zero mean of the fillMap
    non_background_mean = np.mean([x for x in target_map.fullMap.flatten() if x])

    valid_regions = []

    for region in graph.regions:
        total_density = 0
        for node in region.nodes:
            total_density += node.value
        mean_region_density = total_density / len(region.nodes)
        if not (mean_region_density > non_background_mean):
            continue
        standard_deviation = np.std(np.array([x.value for x in region.nodes], dtype=np.float64))
        if not (standard_deviation > STD_THRESHOLD):
            continue
        # Cylinder predicate conditions
        if not (math.sqrt(region.eigenvalues[1]) < 3.5 and math.sqrt(region.eigenvalues[2]) < 3.5):
            continue
        if region.eigenvalues[0] > HELIX_LENGTH_THRESHOLD:
            continue

        # If all of the above are valid, add the region to the final region list
        valid_regions.append(region)
    print "pruned {}".format(len(graph.regions) - len(valid_regions))
    graph.regions = valid_regions


    output_matrix = np.zeros(target_map.box_size())
    for i, region in enumerate(graph.regions):
        for node in region.nodes:
            if node.voxel[1] == 54:
                continue
            output_matrix[node.voxel[0], node.voxel[1], node.voxel[2]] = i+1
        region.id = i+1
    return output_matrix, graph
