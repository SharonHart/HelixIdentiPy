"""
Create templates based on ideal cylinder.
Do so by rotating the cylinder 144 times, 12 times f.e. axis
"""

import utils
import numpy as np
from TEMPy.ScoringFunctions import *
from scipy.ndimage.filters import gaussian_filter
from sklearn.decomposition import PCA

from messages import Messages



def main(apix, cylinder_map, templates_dir, template_format, final_shape, limits):
    """
    :param apix: Input map's apix
    :param cylinder_map: Map instance of the ideal cylinder
    :param templates_dir: Path for writing the templates
    :param template_format: File name format for  the templates
    :return: dict. Vector representation for x and y axis rotations
    """

    vectors_dic = {}
    pc = PCA(n_components=3)

    sanity = 0 # Loop counter

    for i in range(12): # For every x rotation
        rad_in_x = (math.pi / 12) * i  # X axis rotation (in rads)
        for j in range(12): # For every y rotation
            rad_in_y = (math.pi / 12) * j  # Y axis rotation (in rads)

            sanity += 1

            c = cylinder_map.get_com()
            template_cylinder = cylinder_map
            # Rotate in x axis around CoM, by rad_in_x degrees
            template_cylinder = template_cylinder.rotate_by_axis_angle(x=1, y=0, z=0, angle=rad_in_x, CoM=c, rad=True)
            # Rotate in y axis around CoM, by rad_in_y degrees
            template_cylinder = template_cylinder.rotate_by_axis_angle(x=0, y=1, z=0, angle=rad_in_y, CoM=c, rad=True)

            # Smooth template by using gaussian filter. Set Sigma as the map's apix
            cylinder_array = gaussian_filter(template_cylinder.fullMap, sigma=apix)
            template_cylinder.fullMap = cylinder_array
            # resize to original size and patch in the template
            template_cylinder.fullMap = resize_and_place_cylinder(final_shape, limits, template_cylinder)
            # save template to file
            template_cylinder.write_to_MRC_file(templates_dir + template_format.format(i, j))

            # Calculate PC1 (main vector) of the template
            list_points = []
            for (x, y, z), value in np.ndenumerate(template_cylinder.fullMap):
                if value > 0:
                    list_points.append([x, y, z])
            pca = pc.fit(np.array(list_points, dtype=np.float64))
            vectors_dic[(rad_in_x, rad_in_y)] = pca.components_[0]

            # Set progress status in percents
            utils.set_status(Messages.PROGRESS_TEMPLATES.format(str(sanity*100/144)), same_line=True)


    return vectors_dic

def resize_and_place_cylinder(final_shape, limits, template_cylinder):
    X = 2
    Y = 1
    Z = 0
    START = 0
    STOP = 1
    LEFT_PAD = 5
    RIGHT_PAD = 6
    temp_array = np.zeros(final_shape, dtype=np.float64)
    temp_array[limits[START][Z] - LEFT_PAD:limits[STOP][Z] + RIGHT_PAD,
    limits[START][Y] - LEFT_PAD:limits[STOP][Y] + RIGHT_PAD,
    limits[START][X] - LEFT_PAD:limits[STOP][X] + RIGHT_PAD] = template_cylinder.fullMap
    return temp_array
