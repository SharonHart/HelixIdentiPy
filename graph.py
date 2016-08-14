
import math


def graph_creation(score_matrix):

    i_size = len(score_matrix)
    j_size = len(score_matrix[0])
    k_size = len(score_matrix[0,0])

    dict = {}
    index = 0
    for i in range(i_size):
        for j in range(j_size):
            for k in range(k_size):
                if (score_matrix[i,j,k] >= 0.3):
                    dict[index] = ([i,j,k],None)
                    index = index+1

    neighbors_matrix_size = len(dict)
    ## defining a zero matrix for the neighboring matrix
    neighbors_matrix = [[0 for col in range (neighbors_matrix_size)]  for row in range (neighbors_matrix_size)]

    regions = [][]
    regions_index = 0
    cross = 0

    ## creating the graph. connecting two vertecies is equal to putting 1 in the relevant box
    for row in range (neighbors_matrix_size):
        for col in range(cross):

            ##getting the voxels
            voxel1 = dict[row][0]
            voxel2 = dict[col][0]

            if is_neighbors(voxel1,voxel2) and is_teta_parralel(voxel1,voxel2,max_dir,teta):
                neighbors_matrix[row][col] = 1
                neighbors_matrix[col][row] = 1


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
    if (voxel1[0] - voxel2[0] >= -1 and voxel1[0] - voxel2[0] <= 1):
        if (voxel1[1] - voxel2[1] >= -1 and voxel1[1] - voxel2[1] <= 1):
            if (voxel1[2] - voxel2[2] >= -1 and voxel1[2] - voxel2[2] <= 1):
                return True
    return False

def is_teta_parralel_pythagoras(voxel1, voxel2, directions, teta):
    radian_change_x = directions(voxel1)[0] - directions(voxel2)[0]
    radian_change_y = directions(voxel1)[1] - directions(voxel2)[1]
    angle = pythagoras(radian_change_x,radian_change_y)
    if abs(angle)<teta:
        return True
    else:
        return False


def pythagoras(x,y):
    return math.sqrt((x*x)+(y*y))

def is_teta_parralel(voxel1, voxel2, directions, teta):
    radian_change_x = directions(voxel1)[0] - directions(voxel2)[0]
    radian_change_y = directions(voxel1)[1] - directions(voxel2)[1]
    if abs(radian_change_x) <= teta and abs(radian_change_y) <= teta:
        return True
    else:
        return False

