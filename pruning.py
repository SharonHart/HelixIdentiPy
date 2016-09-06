"""
Prune the resulted regions, removing non-alpha-helical resembling regions.
Returns the final matrix.
A cell with value 0 was found to be non-helix, otherwise, we assign 1-N id for each region and a cell assigned to it.
"""
import numpy as np


def main(graph, matrix_size):
    output_matrix = np.zeros(matrix_size)
    for i, region in enumerate(graph.regions):
        for node in region.nodes:
            if node.voxel[1] == 54:
                continue
            output_matrix[node.voxel[0], node.voxel[1], node.voxel[2]] = i+1
        region.id = i+1
    return output_matrix
