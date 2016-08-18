from TEMPy.ScoringFunctions import *
from scipy.ndimage.filters import gaussian_filter
import os

from messages import Messages

""""generates templates"""


def main(target_map, cylinder_map, overwrite=False):

    print Messages.START_TEMPLATES

    cylinder_array = cylinder_map.fullMap
#
 #   # smooth cylinder by gaussian mask TODO: figure out how to get sigma and what function to use
    sigma = target_map.apix
    # cylinder_array = gaussian_filter(cylinder_array, sigma)

    # cylinder_map.fullMap = cylinder_array
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory = dir_path + "/Templates"
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        # don't do unnecessary work
        if (not overwrite) and len(os.listdir(directory)) >= 144:
            print Messages.TEMPLATES_EXIST
            return


    sanity = 0
    for i in range(12):  # for every x rotation
        rad_in_x = (math.pi / 12) * i  # x axis rotation (in rads)
        for j in range(12):  # for every y rotation
            rad_in_y = (math.pi / 12) * j  # y axis rotation (in rads)
            template_cylinder = cylinder_map.rotate_by_axis_angle(x=1, y=0, z=0, angle=rad_in_x, CoM=cylinder_map.get_com(), rad=True)
            template_cylinder = template_cylinder.rotate_by_axis_angle(x=0, y=1, z=0, angle=rad_in_y, CoM=template_cylinder.get_com(), rad=True)
            cylinder_array = gaussian_filter(template_cylinder.fullMap, sigma)
            template_cylinder.fullMap = cylinder_array
            template_cylinder.write_to_MRC_file(directory + "/template{0}_{1}.mrc".format(i, j))

            sanity += 1
    print Messages.DONE_TEMPLATES.format(sanity)

