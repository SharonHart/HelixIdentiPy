import math
from classes import *

# create graph instance
graph = Graph()
directions = None
scores = None
theta = math.pi / 9

APIX = None

def graph_creation(score_matrix, max_dir, dic_directions,theta_arg, apix, THRESHOLD=None):
    global APIX
    APIX = apix
    global theta
    theta = theta_arg
    if not THRESHOLD:
        N = 8000
        THRESHOLD = np.percentile(score_matrix, 100 - ((float(N) / score_matrix.size) * 100))
    if 0 < THRESHOLD <= 1:
        score_matrix /= score_matrix.max()
    if len(score_matrix)<3 or len(max_dir) < 3:
        print "no good"

    # create nodes that are above threshold
    # create region foreach new node
    # append to graph
    for (x,y,z), value in np.ndenumerate(score_matrix):
        if value >= THRESHOLD:
            region = Region()
            node = Node([x,y,z], max_dir[x,y,z], dic_directions[max_dir[x,y,z][0],max_dir[x,y,z][1]], value, region=region)
            region.nodes.append(node)
            graph.nodes.append(node)
            graph.regions.append(region)

    # foreach pair of nodes check if they should be connected and appended to region todo:  this is a naive impl change for a better one
    for i in range(len(graph.nodes)):
        node1 = graph.nodes[i]
        for j in range(i+1, len(graph.nodes)):
            node2 = graph.nodes[j]
            if should_connect(node1, node2):
                print i,j
                connect(node1, node2)
    return graph


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
    # v1 = np.append(node1.direction, [1])
    # v2 = np.append(node2.direction, [1])
    return angle(node1.pca_dir, node2.pca_dir)*57.2958 <= theta


def pairwise_region_parallelism(region1, region2, theta):
    for node1 in region1.nodes: # todo  this is naive
        for node2 in region2.nodes:
            if not theta_parallel(node1, node2, theta): return False
    return True


def region_pca_parallelism(region, theta=20): #   how to calc angle between pca and nodes direction
    if len(region.nodes) == 0:
        pass
    try:
        region.calc_pca()
    except Exception as e:
        print "pca problem fuck this shit"
        return False
    for node in region.nodes:
        if region.pca and angle(node.pca_dir, region.pca.components_[0])*57.2958 > theta:
            return False
    print "hallelujah!"
    return True

def is_theta_parallel(node1, node2, theta=20):
    r1 = node1.region
    r2 = node2.region

    # same region
    if r1 == r2: return False

    # regions are small - still no PCA
    if (len(r1.nodes) + len(r2.nodes)) <= 8:
        return pairwise_region_parallelism(r1, r2, theta)

    # need to check pca
    else:
        r_new = Region()
        r_new.nodes = r1.nodes + r2.nodes
        return region_pca_parallelism(r_new)

def is_predicate_verified(node1, node2): #todo
    r1 = node1.region
    r2 = node2.region

    # same region
    if r1 == r2: return False

    # regions are small - still no PCA
    if (len(r1.nodes) + len(r2.nodes)) <= 8:
        return True

    # need to check pca
    else:
        new_region = Region()
        new_region.nodes = r1.nodes + r2.nodes
        new_region.calc_pca()
        lambda_1, lambda_2, lambda_3 = tuple(new_region.eigenvalues)
        return math.sqrt(lambda_2) <= 3.5/APIX and math.sqrt(lambda_3) <= 3.5/APIX



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
    if len(r_new.nodes) > 8:
        try:
            r_new.calc_pca()
        except Exception as e:
            print "pca problem fuck this shit22222"
    for node in r_new.nodes:
        node.region = r_new

def connect_regions(node1, node2):
    if node1.region == node2.region:
        print "tried to connect two similar regions!"
        return
    r_new = Region()
    r_new.nodes = node1.region.nodes + node2.region.nodes
    if len(r_new.nodes) > 8:
        try:
            r_new.calc_pca()
        except Exception as e:
            print "pca problem fuck this shit22222"
    for node in r_new.nodes:
        node.region = r_new
    return r_new


