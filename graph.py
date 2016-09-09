"""
Create graph with nodes as good scores voxels.
Connect nodes under correct algorithm restrictions.
"""

import math

import utils
from classes import *
from messages import Messages

def main(target_map, score_matrix, max_dir, dic_directions,theta_arg, thresh=None):
    """
    :param score_matrix: scoring matrix from correlation stage
    :param max_dir: directions matrix from the correlation stage
    :param dic_directions: directions dict. from templates stages
    :param theta_arg: the angle allowed between regional nodes
    :param thresh: The threshold by which a voxel is inserted to the graph.
    can be a number greater than 1 for number of nodes or lower than 1 for percentile
    :return: The resulted graph instance
    """
    apix = target_map.apix
    theta = theta_arg
    graph = Graph()

    # Default threshold
    if not thresh:
        N = 1000
        THRESHOLD = np.percentile(score_matrix, 100 - ((float(N) / score_matrix.size) * 100))

    # Percentile option
    elif 0 <= thresh <= 1:
        THRESHOLD = thresh
        score_matrix /= score_matrix.max()

    # Number of voxels to insert option
    else:
        THRESHOLD = np.percentile(score_matrix, 100 - ((float(thresh) / score_matrix.size) * 100))

    # Create nodes that are above threshold
    # Create region foreach new node
    # Append to graph
    for (x,y,z), value in np.ndenumerate(score_matrix):
        if value >= THRESHOLD:
            region = Region()
            node = Node(target_map.fullMap[x,y,z], [x,y,z], max_dir[x,y,z], dic_directions[max_dir[x,y,z][0],max_dir[x,y,z][1]], value, region=region)
            region.nodes.append(node)
            graph.nodes.append(node)
            graph.regions.append(region)

    # Foreach pair of nodes check if they should be connected and appended to region
    for i in range(len(graph.nodes)):
        node1 = graph.nodes[i]
        for j in range(i+1, len(graph.nodes)):
            node2 = graph.nodes[j]
            if should_connect(node1, node2,theta, apix):
                # Connect the nodes
                connect(graph, node1, node2)
                # Show graph progress
                utils.set_status(Messages.GRAPH_PROGRESS.format(i*100/len(graph.nodes)),same_line=True)
    return graph


def is_neighbours(node1, node2):
    """
    Check if both nodes are neighbours. Mainly, if their voxels are near each other
    :param node1: Node
    :param node2: Node
    :return: boolean
    """
    return (node1.voxel[0] - node2.voxel[0] >= -1 and node1.voxel[0] - node2.voxel[0] <= 1) and \
            (node1.voxel[1] - node2.voxel[1] >= -1 and node1.voxel[1] - node2.voxel[1] <= 1) and \
                (node1.voxel[2] - node2.voxel[2] >= -1 and node1.voxel[2] - node2.voxel[2] <= 1)


def unit_vector(v1):
    """
    Get a unit vector of a node's dir.
    :return: float
    """
    return v1/ np.linalg.norm(v1)


def angle(v1, v2):
    """
    Get the angle (rad) between two node vectors
    :return: float
    """
    # Normalize vectors
    v1_u, v2_u = unit_vector(v1), unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def theta_parallel(node1, node2, theta):
    """
    Check if the angle between two nodes is below theta.
    :param node1: Node
    :param node2: Node
    :param theta: float. Angle
    :return: boolean
    """
    return angle(node1.pca_dir, node2.pca_dir)*57.2958 <= theta


def pairwise_region_parallelism(region1, region2, theta):
    """
    Check is the angle between all region nodes of two regions, is below theta
    :param region1: Region
    :param region2: Region
    :param theta: float. Angle
    :return: boolean
    """
    for node1 in region1.nodes:
        for node2 in region2.nodes:
            if not theta_parallel(node1, node2, theta): return False
    return True


def region_pca_parallelism(region, theta=20):
    """
    Check if all the nodes in the region are theta par. to its main vector
    :param region: Graph region
    :param theta: float. Angle
    :return: boolean
    """
    try:
        region.calc_pca()
    except Exception as e:
        return False
    # Check if the angle of each node in the region, is theta parallel to its main vector direction
    for node in region.nodes:
        if region.pca and angle(node.pca_dir, region.pca.components_[0])*57.2958 > theta:
            return False
    return True

def is_theta_parallel(node1, node2, theta):
    """
    Check theta parallelism of two nodes.
    If the combined region of the nodes is smaller than 8 nodes, check angle between all nodes
     Otherwise, check that every node is theta parallel to the region's main vector dir.
    :param node1: Node
    :param node2: Node
    :param theta: float. Angle
    :return: boolean
    """
    r1 = node1.region
    r2 = node2.region

    # Same region
    if r1 == r2: return False

    # Regions are small - still no PCA. Check angle between all nodes of noth regions
    if (len(r1.nodes) + len(r2.nodes)) <= 8:
        return pairwise_region_parallelism(r1, r2, theta)

    # Check with pca calculations
    else:
        r_new = Region()
        r_new.nodes = r1.nodes + r2.nodes
        return region_pca_parallelism(r_new)

def eigenvalues_satisfied(node1, node2, APIX):
    """
    Check if connecting both nodes satisfies predicate cond.
    Check if principle components lengths fit those of a helix
    :return: boolean
    """
    r1 = node1.region
    r2 = node2.region

    # Same region. Should not get here anyway
    if r1 == r2: return False

    # Regions are small - still no PCA
    if (len(r1.nodes) + len(r2.nodes)) <= 8:
        return True

    # Check unified region's PCA
    else:
        new_region = Region()
        new_region.nodes = r1.nodes + r2.nodes
        # Calculate new unified pca
        new_region.calc_pca()
        # Get region's eigenvalues (lengthes of the dir. vectors)
        lambda_1, lambda_2, lambda_3 = tuple(new_region.eigenvalues)
        # Check if helix radius satisfies new region
        return math.sqrt(lambda_2) <= 3.5/APIX and math.sqrt(lambda_3) <= 3.5/APIX

def should_connect(node1, node2, theta, APIX):
    """
    Check if node1 and node2 shoud connect.
    They should be neighbours, theta parallel and cylinder predicated verified
    :return: boolean
    """
    return is_neighbours(node1, node2) and is_theta_parallel(node1, node2, theta) and eigenvalues_satisfied(node1, node2, APIX)


def connect(graph, node1, node2):
    """
    Join two Nodes together by removing their regions and adding a combined region
    :param graph: The regional graph
    :param node1: Node obj.
    :param node2: Node obj.
    :return: void. Update graph regions
    """
    edge = (node1, node2)
    graph.edges.append(edge)
    graph.remove_region(node1.region)
    graph.remove_region(node2.region)
    r_new = Region()
    r_new.nodes = node1.region.nodes + node2.region.nodes
    graph.regions.append(r_new)

    # Calculate pca if the region is big enough
    if len(r_new.nodes) > 8:
        try:
            r_new.calc_pca()
        except Exception:
            print "PCA failure"

    # Update nodes pointers to the new region
    for node in r_new.nodes:
        node.region = r_new

