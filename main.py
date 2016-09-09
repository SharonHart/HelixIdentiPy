import os

from TEMPy.MapParser import *

import utils
from correlation import main as correlate
from create_cylinder import main as cylinder_creation
from create_templates import main as create_templates
from graph import main as graph_creation
from linkage import main as link_regions
from messages import Messages
from output_as_map import main as output_as_map
from plot_result import main as plot_matrix
from pruning import main as pruning

dir_path = os.path.dirname(os.path.realpath(__file__))
source_dir = dir_path + "/source/"
templates_dir = dir_path + "/Templates/"
target_path = ""
target_map = None
cylinder_map = None
apix = None

def run_templates(run):
    try:
        if run:
            utils.set_status(Messages.START_CYL)
            cylinder_map = cylinder_creation(target_map, output_path=source_dir + "Cylinder.mrc")
            utils.set_status(Messages.END_CYL)
            utils.set_status(Messages.START_TEMPLATES)
            dic_directions = create_templates(target_map, cylinder_map)
            utils.set_status(Messages.END_TEMPLATES)
            utils.dump(path=source_dir + "dir_directions.p", object=dic_directions)
        else:
            dic_directions = utils.load(path=source_dir + "dir_directions.p")
        return dic_directions
    except Exception as e:
        utils.set_status(Messages.FAIL_TEMPLATES)
        return None

def run_correlation(run):
    try:
        if run:
            # compute correlation
            utils.set_status(Messages.START_CORRELATION)
            max_scores, max_dirs = correlate(target_map)
            utils.dump(path=source_dir + "max_score",object=max_scores ,is_np=True)
            utils.dump(path=source_dir + "max_dirs",object=max_dirs ,is_np=True)
            utils.set_status(Messages.DONE_CORRELATION)
        else:
            max_scores = utils.load(path=source_dir + "max_score", is_np=True)
            max_dirs = utils.load(path=source_dir + "max_dirs", is_np=True)
        return max_scores, max_dirs
    except Exception as e:
        utils.set_status(Messages.FAIL_CORRELATION)
        return None


def run_graph(theta,apix, THRESHOLD, scores, directions, dic_direct, run):
    try:
        if run:
            utils.set_status(Messages.START_GRAPH)
            graph = graph_creation(target_map, scores, directions, dic_direct, theta,apix, THRESHOLD=THRESHOLD)
            utils.set_status(Messages.END_GRAPH)
            utils.dump(path=source_dir + "graph.p", object=graph)
        else:
            graph = utils.load(source_dir + "graph.p")
        return graph
    except Exception as e:
        utils.set_status(Messages.FAIL_GRAPH)
        return None


def run_linkage(run, graph, theta, mid, line, apix):
    try:
        if run:
            utils.set_status(Messages.START_LINK)
            graph2=link_regions(graph, theta, mid, line, apix)
            utils.set_status(Messages.END_LINK)
            utils.dump(path=source_dir + "graph2.p", object=graph2)
        else:
            graph2 = utils.load(source_dir + "graph2.p")
        return graph2
    except Exception as e:
        utils.set_status(Messages.FAIL_LINK)
        return None


def run_pruning(run, graph2, target_map):
    try:
        if run:
            utils.set_status(Messages.START_PRUN)
            output, graph3 = pruning(graph2, target_map)
            utils.set_status(Messages.END_PRUN)
            utils.dump(path=source_dir + "output", object=output, is_np=True)
            utils.dump(path=source_dir + "graph3.p", object=graph3, is_np=False)

        else:
            output = utils.load(path=source_dir + "output", is_np=True)
            graph3 = utils.load(path=source_dir + "graph3.p", is_np=False)
        return output, graph3
    except Exception as e:
        utils.set_status(Messages.FAIL_PRUN)
        return None


def back_main(thresh, theta, mid, line, start, target_path):
    utils.set_status(Messages.BUMPED_BACK)
    main(thresh, theta, mid, line, start, target_path)


def main(thresh, theta, mid, line, start, input_path):
    """ Calls the main algorithm stages
    :param thresh: Threshold for adding voxels as nodes in the regional graph
    :param theta: The allowed angle between two graph nodes
    :param mid: Midpoint distance for the linkage stage
    :param line: Line distance for the linkage stage
    :param start: Algorithm start point for parameters changing during run
           0: all, 1:after create template, 2:after correlation, 3: after graph, 4: just plot
    :param input_path: Path for the target map file
    :return: Method. Plots the resulted graph and matrix
    """
    utils.set_status(Messages.START_RUN)
    global target_path
    target_path = input_path

    # Create projects directories for intermidiate file savings
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)


    # Read map files
    try:
        global target_map
        target_map = MapParser.readMRC(input_path)
        apix = target_map.apix  # Target map resolution

        # cylinder_map = MapParser.readMRC(source_dir + "Cylinder.mrc")
    except:
        print Messages.INPUT_FILES_ERROR


    # Generate templates
    dic_directions = run_templates(run=True if start<1 else False)
    # if dic_directions is None and start > 0: back_main(thresh, theta, mid, line, start-1, target_path)

    max_scores, max_dirs = run_correlation(run=True if start<2 else False)

    graph = run_graph(run=True if start<3 else False, scores=max_scores,directions= max_dirs,dic_direct=dic_directions,
                      theta=theta, apix=apix, THRESHOLD=thresh)
    graph2 = run_linkage(run=True if start<4 else False, graph=graph, theta=theta, mid=mid, line=line, apix=apix)

    output, graph3 = run_pruning(run=True if start<5 else False, graph2=graph2, target_map=target_map)

    utils.set_status(Messages.END_RUN.format(len(graph2.regions)))


    output_as_map(graph3, target_map)

    plot_matrix(graph3, target_map.box_size())

    return output


if __name__ == "__main__":
    main()