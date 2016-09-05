import os
import global_vars
import pickle
import numpy as np
from TEMPy.MapParser import *
from messages import Messages
from create_templates import main as create_templates
from correlation import main as correlate
from create_cylinder import main as create_cylinder
from graph import main as graph_creation
from linkage import main as link_regions
from plot_result import main as plot_matrix
from pruning import main as pruning

dir_path = os.path.dirname(os.path.realpath(__file__))
source_dir = dir_path + "/source/"
templates_dir = dir_path + "/Templates/"

def run_linkage(theta, mid, line, apix):
    try:
        with open(source_dir + "/graph.p", 'rb') as g:
            graph_prev = pickle.load(g)
        set_status(Messages.START_LINK)
        graph=link_regions(graph_prev, theta, mid, line, apix)
        set_status(Messages.END_LINK)
        with open(dir_path + "/source/graph2.p", 'wb') as f:
            pickle.dump(graph, f)
        return graph
    except IOError:
        return None


def run_graph(theta,apix, THRESHOLD):
    try:
        scores = np.load(source_dir + "/max_score")
        directions = np.load(source_dir + "/max_dirs")
        with open(source_dir + "/dir_directions.p", 'rb') as g:
            dic_direct = pickle.load(g)
        set_status(Messages.START_GRAPH)
        graph = graph_creation(scores, directions, dic_direct, theta,apix, THRESHOLD=THRESHOLD)
        set_status(Messages.END_GRAPH)
        with open(source_dir + "/graph.p", 'wb') as f:
            pickle.dump(graph, f)
        return graph
    except IOError:
        return None


def run_templates(target_map, cylinder_map, overwrite):
    # try:
        set_status(Messages.START_TEMPLATES)
        dic_directions = create_templates(target_map, cylinder_map, overwrite=True)
        set_status(Messages.END_TEMPLATES)
        return dic_directions
    # except IOError:
    #     return None


def set_status(stat):
    if global_vars.isGui:
        global_vars.status_bar.set(stat)
    else:
        print stat


def main(thresh, theta, mid, line, start, target_path):
    """ Calls the main algorithm stages
    :param thresh: Threshold for adding voxels as nodes in the regional graph
    :param theta: The allowed angle between two graph nodes
    :param mid: Midpoint distance for the linkage stage
    :param line: Line distance for the linkage stage
    :param start: Algorithm start point for parameters changing during run
           0: all, 1:after create template, 2:after correlation, 3: after graph, 4: just plot
    :param target_path: Path for the target map file
    :return: Method. Plots the resulted graph and matrix
    """

    set_status(Messages.START_RUN)

    # Create projects directories for intermidiate file savings
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    # Read the target map file.
    try:
        target_map = MapParser.readMRC(target_path)
        apix = target_map.apix  # Target map resolution
    except Exception as e:
       print Messages.INPUT_FILES_ERROR

    # Create the ideal cylinder.
    set_status(Messages.START_CYL)
    cylinder_map = create_cylinder(target_map)
    cylinder_map.write_to_MRC_file(source_dir + "Cylinder.mrc")
    set_status(Messages.END_CYL)

    if start < 1 or len(os.listdir(templates_dir)) < 144:
        # Generate templates
        dic_directions = run_templates(target_map, cylinder_map, overwrite=True)
    else:
        try:
            with open(source_dir + "dir_directions.p") as g:
                dic_directions = pickle.load(g)
        except IOError:
            if start > 0:
                set_status(Messages.BUMPED_BACK)
                return main(thresh, theta, mid, line, start-1, target_path)





    if start < 2 or (not (os.path.isfile(source_dir + "max_score"))):
        try:
            # compute correlation
            set_status(Messages.START_CORRELATION)
            max_score, max_dirs = correlate(target_map)
            set_status(Messages.DONE_CORRELATION)
        except IOError:
            if start > 0:
                set_status(Messages.BUMPED_BACK)
                return main(thresh, theta, mid, line, start-1, target_path)
    if start < 3:
        graph = run_graph(theta, apix, THRESHOLD=thresh)
    else:
        try:
            with open(source_dir + "graph.p", 'rb') as g:
                graph = pickle.load(g)
        except IOError:
            graph = run_graph(theta,apix, THRESHOLD=thresh)
            if graph == None:
                if start > 0:
                    set_status(Messages.BUMPED_BACK)
                    return main(thresh, theta, mid, line, start - 1, target_path)
                else:
                    return
    if start < 4:
        graph2 = run_linkage(theta, mid, line, apix)
    else:
        try:
            with open(source_dir + "graph2.p", 'rb') as g:
                graph2 = pickle.load(g)
        except IOError:
            graph2 = run_linkage(theta, mid, line, apix)
            if graph2 == None:
                if start > 0:
                    set_status(Messages.BUMPED_BACK)
                    return main(thresh, theta, mid, line, start - 1, target_path)
                else:
                    return

    output = pruning(graph2, cylinder_map.box_size())
    set_status(Messages.END_RUN)

    plot_matrix(graph2, target_map.box_size())

if __name__ == "__main__":
    main()