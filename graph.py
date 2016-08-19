import math
import numpy as np

THETA = math.pi * 20 / 180

def graph_creation(score_matrix, dir_matrix):

    i_size, j_size, k_size = score_matrix.shape

    dict = {}
    index = 0

    # indices = ((score_matrix > 50)).nonzero()
    for (x, y, z), value in np.ndenumerate(score_matrix):
        if value >= 50:
            dict[index] = ([x, y, z], None)
            index += 1

    # for i in range(i_size):
    #     for j in range(j_size):
    #         for k in range(k_size):
    #             if (score_matrix[i,j,k] >= 50):
    #                 dict[index] = ([i,j,k], None)
    #                 index = index + 1

    neighbors_matrix = np.zeros((len(dict), len(dict)))
    #neighbors_matrix_size = len(dict)
    ## defining a zero matrix for the neighboring matrix
    #neighbors_matrix = [[0 for col in range (neighbors_matrix_size)]  for row in range (neighbors_matrix_size)]

    regions_index = 0
    cross = 0

    ## creating the graph. connecting two vertecies is equal to putting 1 in the relevant box
    for row in range (neighbors_matrix.shape[0]):
        for col in range(cross):

            ##getting the voxels
            voxel1 = dict[row][0]
            voxel2 = dict[col][0]

            if is_neighbors(voxel1,voxel2) and is_theta_parallel(dir_matrix[voxel1], dir_matrix[voxel2], THETA):
                neighbors_matrix[row][col] = 1
                neighbors_matrix[col][row] = 1

        cross = cross + 1

def regions_creation(neighbors_matrix):

    main_queue = [None for index in range (len(matrix[0]))]
    temp_queue = []
    size = len(main_queue)
    region = 0

    for i in range (size):

        ##if the voxel isn't already in a group
        if main_queue[i] is None:

            ##initialize the temp queue to hold the neighbors
            for j in range(size):
                if neighbors_matrix[i][j] is 1:
                    temp_queue.insert(j)
                    main_queue[j] = region

            ##updating the temp queue to hold all the neighbors
            while temp_queue:
                i = temp_queue.pop(0)
                for j in range(size):
                    if neighbors_matrix[i][j] is 1:
                        if main_queue[j] is None:
                            main_queue[j] = region
                            temp_queue.insert(-1, j)

            region = region + 1



def is_neighbors(voxel1, voxel2):
    return (voxel1[0] - voxel2[0] >= -1 and voxel1[0] - voxel2[0] <= 1) and \
        (voxel1[1] - voxel2[1] >= -1 and voxel1[1] - voxel2[1] <= 1) and \
        (voxel1[2] - voxel2[2] >= -1 and voxel1[2] - voxel2[2] <= 1)


def is_theta_parallel(v1, v2, theta):
    v1 = np.append(v1, [1])
    v2 = np.append(v2, [1])
    print v1, v2
    return angle_between(v1, v2) <= theta

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """
    :param v1: 1st vector
    :param v2: 2nd vector
    :return: the angle between the vectors
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
