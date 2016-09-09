""""
Correlates between the target map and the generated templates.
Returns a score matrix and a direction matrix holding the best directions f.e. voxel
"""

import os

import numpy as np
from TEMPy.MapParser import *
from TEMPy.ScoringFunctions import *

from messages import Messages


def main(target_map):
    max_scores = np.zeros(target_map.box_size())
    max_dirs = np.zeros(target_map.box_size(), dtype=(float, 2))
    dir_path = os.path.dirname(os.path.realpath(__file__))

    templates_dir = dir_path + "/Templates"
    target_map.fullMap = target_map.fullMap / target_map.fullMap.max()

    for i in range(12):  # for every x rotation
        rad_in_x = (math.pi / 12) * i  # y axis rotation (in rads)
        for j in range(12):  # for every y rotation
            rad_in_y = (math.pi / 12) * j  # y axis rotation (in rads)
            template_name = "/template{0}_{1}.mrc".format(i, j)
            print template_name
            try:
                template_cylinder = MapParser.readMRC(templates_dir + template_name)
            except Exception as e:
                print e
                print Messages.ERROR_READING_TEMPLATE_FILE.format(template_name)

            template = template_cylinder
            try:
                correlation_matrix = np.fft.ifftn(np.multiply(np.fft.fftn(target_map.fullMap), np.conj(np.fft.fftn(template_cylinder.fullMap))))
                # python's / MATLAB ifft returns malformed matrix. Issue fixed by running fftshift
                correlation_matrix = np.fft.fftshift(correlation_matrix)

                # save the maximal value and direction for each voxel
                for (x, y, z), value in np.ndenumerate(correlation_matrix):
                    if value > max_scores[x, y, z]:
                        max_scores[x, y, z] = value
                        max_dirs[x, y, z] = (rad_in_x, rad_in_y)

            except Exception as e:
                Messages.CORRELATION_ERROR.format(template_name) + e.message

    return max_scores, max_dirs
