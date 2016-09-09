""""
Correlates between the target map and the generated templates.
Returns a score matrix and a direction matrix holding the best directions f.e. voxel
"""

import math
import os

import numpy as np
from TEMPy.MapParser import *

import utils
from messages import Messages


def main(target_map, templates_dir, template_format):
    """
    :param target_map: Map instance of the target line
    :param templates_dir: The directory path of the cylinder templates
    :return: max_scores, max_dirs. numpy arrays. max score fitting direction for each voxel
    """
    max_scores = np.zeros(target_map.box_size())
    max_dirs = np.zeros(target_map.box_size(), dtype=(float, 2))

    target_matrix = target_map.fullMap / target_map.fullMap.max()

    sanity = 0 # Loop counter
    for i in range(12):  # For every x rotation
        rad_in_x = (math.pi / 12) * i  # Y axis rotation (in rads)
        for j in range(12):  # For every y rotation
            rad_in_y = (math.pi / 12) * j  # Y axis rotation (in rads)
            sanity += 1

            template_name = template_format.format(i, j)
            try:
                template_cylinder = MapParser.readMRC(templates_dir + template_name)
            except Exception as e:
                utils.set_status( Messages.ERROR_READING_TEMPLATE_FILE.format(template_name))

            try:
                # Calculate Cross Correlation
                correlation_matrix = np.fft.ifftn(np.multiply(np.fft.fftn(target_matrix), np.conj(np.fft.fftn(template_cylinder.fullMap))))

                # !!! Python's / MATLAB ifft returns malformed matrix. Issue fixed by running fftshift !!!
                correlation_matrix = np.fft.fftshift(correlation_matrix)

                # Save the maximal value and direction for each voxel
                for (x, y, z), value in np.ndenumerate(correlation_matrix):
                    if value > max_scores[x, y, z]:
                        max_scores[x, y, z] = value
                        max_dirs[x, y, z] = (rad_in_x, rad_in_y)

                # Print correlation progress
                utils.set_status(Messages.CORRELATION_PROGRESS.format(str(sanity*100/144)),same_line=True)

            except Exception as e:
                utils.set_status(Messages.CORRELATION_ERROR.format(template_name) + e.message)

    return max_scores, max_dirs
