import os
import utils
import numpy as np
from TEMPy.ScoringFunctions import *
from scipy.ndimage.filters import gaussian_filter
from sklearn.decomposition import PCA

from messages import Messages

""""generates templates"""


def main(target_map, cylinder_map):
    dic = {}
    pc = PCA(n_components=3)

    #   # smooth cylinder by gaussian mask
    sigma = target_map.apix

    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory = dir_path + "/Templates"
    sanity = 0

    # for every x rotation
    for i in range(12):
        rad_in_x = (math.pi / 12) * i  # x axis rotation (in rads)
        # for every y rotation
        for j in range(12):
            rad_in_y = (math.pi / 12) * j  # y axis rotation (in rads)

            c = cylinder_map.get_com()
            template_cylinder = cylinder_map.rotate_by_axis_angle(x=1, y=0, z=0, angle=rad_in_x, CoM=c, rad=True)
            template_cylinder = template_cylinder.rotate_by_axis_angle(x=0, y=1, z=0, angle=rad_in_y, CoM=c, rad=True)

            list_points = []
            for z in range(template_cylinder.fullMap.shape[0]):
                for y in range(template_cylinder.fullMap.shape[1]):
                    for x in range(template_cylinder.fullMap.shape[2]):
                        if template_cylinder.fullMap[z][y][x] > 0:
                            list_points.append([z, y, x])
            pca = pc.fit(np.array(list_points, dtype=np.float64))
            dic[(rad_in_x, rad_in_y)] = pca.components_[0]
            cylinder_array = gaussian_filter(template_cylinder.fullMap, sigma)
            template_cylinder.fullMap = cylinder_array
            template_cylinder.write_to_MRC_file(directory + "/template{0}_{1}.mrc".format(i, j))
            sanity += 1
            utils.set_status(Messages.PROGRESS_TEMPLATES.format(str(sanity*100/144)))
    return dic
