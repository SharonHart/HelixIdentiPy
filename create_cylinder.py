# ===========================================================================================
# This example read a density map and performs operations such as translation, rotation, etc.
# ===========================================================================================
import numpy as np
from TEMPy.MapParser import MapParser
from TEMPy.StructureParser import PDBParser
import os

from matplotlib.mlab import PCA


def cylinder_creation(path):

    path_out = './source/'
    if os.path.exists(path_out) == True:
        print "%s exists" % path_out
    else:
        os.mkdir(path_out)
    #os.chdir(path_out)

    # Example of user defined parameters
    sim_res = 6.6  # Target resolution of the outputted map.
    sim_sigma_coeff = 0.187  # Sigma width of the Gaussian used to blur the atomic structure.

    # structure_instance = PDBParser.read_PDB_file('1J6Z', '/home/bar/Downloads/1j6z.pdb', hetatm=False, water=False)
    # print structure_instance

    map_target = MapParser.readMRC(path)  # read target map
    # map_target3 = map_target.translate(5.2, 5, 1)  # Translation. Uses fourier-shifting, so movements are periodic.
    # map_target4 = map_target.normalise()  # Normalising (mean=0, sd=1)

    # MARK addition for students
    # 1. Save Map after translations
    map_target.write_to_MRC_file(path_out + 'Map_After_Processing.mrc')

    # 2 Very very simple example of the cylinder
    dr = 2.3  # radius of the cylinder
    h = 10.8  # height of the cylinder
    rho = 1  # density of the cylinder

    map_target.shift_origin(0, 0, 0)

    dz = len(map_target.fullMap) * map_target.apix / 2
    dy = len(map_target.fullMap[0]) * map_target.apix / 2
    dx = len(map_target.fullMap[0][0]) * map_target.apix / 2
    points_array = []
    for z in range(len(map_target.fullMap)):
        for y in range(len(map_target.fullMap[z])):
            for x in range(len(map_target.fullMap[z][y])):
                z_coor = z * map_target.apix - dz
                y_coor = y * map_target.apix - dy
                x_coor = x * map_target.apix - dx

                if (z_coor < h) & (z_coor > 0) & (y_coor * y_coor + x_coor * x_coor < dr * dr):
                    map_target.fullMap[z][y][x] = rho
                    points_array.append([z,y,x])
                else:
                    map_target.fullMap[z][y][x] = 0

    map_target.write_to_MRC_file(path_out + 'Cylinder.mrc')


    pca = PCA(np.array(points_array, dtype=np.float64), standardize=False)
    print "bla"
    print pca.Wt[0]