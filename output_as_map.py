"""
Output the result as a map file.
For each voxel that is related to a region, the density value is 1
For a voxel that is not part of a region, the density value is 0
"""

import numpy as np
from TEMPy.MapParser import *

def main(graph, target_map):
    target_fullmap = np.zeros(target_map.box_size())
    for i, region in enumerate(graph.regions):
        for node in region.nodes:
            target_fullmap[node.voxel[0], node.voxel[1], node.voxel[2]] = 1
    target_map.fullMap = target_fullmap
    target_map.write_to_MRC_file("out_map.mrc")