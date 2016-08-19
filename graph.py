import random

from classes import *

# create graph instance
graph = Graph()
directions = None
scores = None

def graph_creation(score_matrix, max_dir, THRESHOLD=70):

    scores = score_matrix
    directions = max_dir
    if len(score_matrix)<3 or len(max_dir) < 3:
        print "no good"

    # create nodes that are above threshold
    # create region foreach new node
    # append to graph
    for (x,y,z), value in np.ndenumerate(score_matrix):
        if value >= THRESHOLD:
            region = Region()
            node = Node([x,y,z], max_dir[x,y,z], value, region=region)
            region.nodes.append(node)
            graph.nodes.append(node)
            graph.regions.append(region)

    # foreach pair of nodes check if they should be connected and appended to region todo:  this is a naive impl change for a better one
    # for node1 in graph.nodes:
    #     for node2 in graph.nodes:
    #         if node1 == node2: pass
    #         if should_connect(node1, node2):
    #             connect(node1, node2)
    for i in range(len(graph.nodes)):
        node1 = graph.nodes[i]
        for j in range(i+1, len(graph.nodes)):
            node2 = graph.nodes[j]
            if should_connect(node1, node2):
                connect(node1, node2)

    print "done!"
def is_neighbours(node1, node2):
    return (node1.voxel[0] - node2.voxel[0] >= -1 and node1.voxel[0] - node2.voxel[0] <= 1) and \
            (node1.voxel[1] - node2.voxel[1] >= -1 and node1.voxel[1] - node2.voxel[1] <= 1) and \
                (node1.voxel[2] - node2.voxel[2] >= -1 and node1.voxel[2] - node2.voxel[2] <= 1)


def unit_vector(v1):
    return v1/ np.linalg.norm(v1)


def angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def theta_parallel(node1, node2, theta):
    v1 = np.append(node1.direction, [1])
    v2 = np.append(node2.direction, [1])
    return angle(v1, v2) <= theta


def pairwise_region_parallelism(region1, region2, theta):
    for  node1 in region1.nodes: # todo  this is naive
        for node2 in region2.nodes:
            if not theta_parallel(node1, node2, theta): return False
    return True


def region_pca_parallelism(region): #todo   how to calc angle between pca and nodes diretion

    region.calc_pca()
    # for node in region.nodes:
        # v1 = np.append(node.direction
        # if angle(node.)
        # return False
    return True if random.random() <=0.5 else False

def is_theta_parallel(node1, node2, theta=20):
    r1 = node1.region
    r2 = node2.region

    # same region
    if r1 == r2: return False

    # regions are small - still no PCA
    if (len(r1.nodes) + len(r2.nodes)) < 8:
        return pairwise_region_parallelism(r1, r2, theta)

    # need to check pca
    else:
        r_new = Region()
        r_new.nodes = r1.nodes + r2.nodes
        return region_pca_parallelism(r_new)

def is_predicate_verified(node1, node2): #todo
    return True if random.random() > 0.5 else False


def should_connect(node1, node2):
    return is_neighbours(node1, node2) and is_theta_parallel(node1, node2) and is_predicate_verified(node1, node2)


def connect(node1, node2):
    edge = (node1, node2)
    graph.edges.append(edge)
    if node1.region == node2.region:
        print "shit!"
    graph.remove_region(node1.region)
    graph.remove_region(node2.region)
    r_new = Region()
    r_new.nodes = node1.region.nodes + node2.region.nodes
    graph.regions.append(r_new)
    if len(r_new.nodes) >= 8: r_new.calc_pca()
    for node in r_new.nodes:
        node.region = r_new






# --------------------OLD CODE------------------------#

#
#     neighbors_matrix_size = len(dict)
#     ## defining a zero matrix for the neighboring matrix
#     neighbors_matrix = [[0 for col in range (neighbors_matrix_size)]  for row in range (neighbors_matrix_size)]
#
#     #regions = [][]
#     #regions_index = 0
#     cross = 0
#
#     ## creating the graph. connecting two vertecies is equal to putting 1 in the relevant box
#     for row in range (neighbors_matrix_size):
#         for col in range(cross):
#
#             ##getting the voxels
#             voxel1 = dict[row][0]
#             voxel2 = dict[col][0]
#
#             if is_neighbors(voxel1,voxel2) and is_teta_parralel(voxel1,voxel2,max_dir,.35):
#                 neighbors_matrix[row][col] = 1
#                 neighbors_matrix[col][row] = 1
#
#     regions_creation(neighbors_matrix)
#     pass
#
#
#
# def regions_creation(neighbors_matrix):
#
#     main_queue = [None for index in range (len(neighbors_matrix[0]))]
#     temp_queue = []
#     size = len(main_queue)
#     region = 0
#
#     for i in range (size):
#
#         ##if the voxel isn't already in a group
#         if main_queue[i] is None:
#
#             ##initialize the temp queue to hold the neighbors
#             for j in range(size):
#                 if neighbors_matrix[i][j] is 1:
#                     temp_queue.insert(j)
#                     main_queue[j] = region
#
#             ##updating the temp queue to hold all the neighbors
#             while temp_queue:
#                 i = temp_queue.pop(0)
#                 for j in range(size):
#                     if neighbors_matrix[i][j] is 1:
#                         if main_queue[j] is None:
#                             main_queue[j] = region
#                             temp_queue.insert(-1, j)
#
#             region = region + 1
#
#
#
# def is_neighbors(voxel1, voxel2):
#     if (voxel1[0] - voxel2[0] >= -1 and voxel1[0] - voxel2[0] <= 1):
#         if (voxel1[1] - voxel2[1] >= -1 and voxel1[1] - voxel2[1] <= 1):
#             if (voxel1[2] - voxel2[2] >= -1 and voxel1[2] - voxel2[2] <= 1):
#                 return True
#     return False
#
# def is_teta_parralel_pythagoras(voxel1, voxel2, directions, teta):
#     radian_change_x = directions(voxel1)[0] - directions(voxel2)[0]
#     radian_change_y = directions(voxel1)[1] - directions(voxel2)[1]
#     angle = pythagoras(radian_change_x,radian_change_y)
#     if abs(angle)<teta:
#         return True
#     else:
#         return False
#
#
# def pythagoras(x,y):
#     return math.sqrt((x*x)+(y*y))
#
# def is_teta_parralel(voxel1, voxel2, directions, teta):
#     radian_change_x = directions(voxel1)[0] - directions(voxel2)[0]
#     radian_change_y = directions(voxel1)[1] - directions(voxel2)[1]
#     if abs(radian_change_x) <= teta and abs(radian_change_y) <= teta:
#         return True
#     else:
#         return False
#
