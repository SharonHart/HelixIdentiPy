import numpy as np
from TEMPy.ScoringFunctions import *
from sklearn.decomposition import PCA
from scipy.ndimage.filters import gaussian_filter
import os
import pickle
from graph import angle
from scipy.ndimage.interpolation import rotate


from messages import Messages
""""generates templates"""


def main(target_map, cylinder_map, overwrite=False):
    dic = {}
    pc = PCA(n_components=3)
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
            dic = pickle.load(open(dir_path + "/source/d.p"))
            return dic


    sanity = 0

    for i in range(12):  # for every x rotation
        rad_in_x = (math.pi / 12) * i  # x axis rotation (in rads)
        for j in range(12):  # for every y rotation
            rad_in_y = (math.pi / 12) * j  # y axis rotation (in rads)
            print rad_in_x, rad_in_y

            c = cylinder_map.get_com()
            template_cylinder =  cylinder_map
            template_cylinder = cylinder_map.rotate_by_axis_angle(x=1, y=0, z=0, angle=rad_in_x, CoM=c, rad=True)
            # template_cylinder.fullMap = rotate(template_cylinder.fullMap,rad_in_x*57.29, axes=(1,0))
            # template_cylinder.fullMap = rotate(template_cylinder.fullMap,rad_in_y*57.29, axes=(0,1))
            template_cylinder = template_cylinder.rotate_by_axis_angle(x=0, y=1, z=0, angle=rad_in_y, CoM=c, rad=True)
            list_points = []
            for z in range(template_cylinder.fullMap.shape[0]):
                for y in range(template_cylinder.fullMap.shape[1]):
                    for x in range(template_cylinder.fullMap.shape[2]):
                        if template_cylinder.fullMap[z][y][x] > 0:
                            list_points.append([z, y, x])
            #pca = PCA(np.array(list_points, dtype=np.float64), standardize=False)
            pca = pc.fit(np.array(list_points, dtype=np.float64))

            dic[(rad_in_x, rad_in_y)] = pca.components_[0]

            cylinder_array = gaussian_filter(template_cylinder.fullMap, sigma)
            template_cylinder.fullMap = cylinder_array
            template_cylinder.write_to_MRC_file(directory + "/template{0}_{1}.mrc".format(i, j))

            sanity += 1
    print Messages.DONE_TEMPLATES.format(sanity)
    pickle.dump(dic, open(dir_path + "/source" + "/dir_directions.p", 'wb'))
    return dic
