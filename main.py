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
template_format = "template{0}_{1}.mrc"
target_path = ""


def create_project_dirs():
    """
    Create project directories
    """
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

def read_map(input_path):
    """
    Read map file from path, Using TemPy
    :param input_path: input target map path
    :return: target map instance, target map apix
    """
    try:
        target_map = MapParser.readMRC(input_path)
        apix = target_map.apix  # Target map resolution
        return target_map, apix
    except:
        print Messages.INPUT_FILES_ERROR


def run_templates(target_map_path, run):
    """
    Creates ideal cylinder and templates based on its rotations
    :param run: boolean. Whether to run again or load rel. files
    :return: dict. directions, with direction: pc1 as key: value
    """
    try:
        if run:
            target_map, apix = read_map(target_path)
            utils.set_status(Messages.START_CYL)
            cylinder_map = cylinder_creation(target_map)
            cylinder_map.write_to_MRC_file(source_dir + "Cylinder.mrc")
            utils.set_status(Messages.END_CYL)
            utils.set_status(Messages.START_TEMPLATES)
            dic_directions = create_templates(target_map.apix, cylinder_map, templates_dir, template_format)
            utils.set_status(Messages.END_TEMPLATES)
            utils.dump(path=source_dir + "dir_directions.p", object=dic_directions)
        else:
            dic_directions = utils.load(path=source_dir + "dir_directions.p")
        return dic_directions
    except Exception as e:
        utils.set_status(Messages.FAIL_TEMPLATES)
        return None


def run_correlation(target_map, run):
    """
    Runs Cross-Correlation stage. finds maximal scored direction for each matrix voxel.
    Saves results, max_score and max_dirs, as np objects
    :param run: boolean. Whether to run again or load rel. files
    :return: max_score and max_dirs, for maximum score and its fitting maximal direction f.e. voxel.
    """
    try:
        if run:
            utils.set_status(Messages.START_CORRELATION)
            max_scores, max_dirs = correlate(target_map, templates_dir, template_format)
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


def run_graph(target_map, run, theta, THRESHOLD, scores, directions, dic_direct):
    """
    Runs Graph creation and Nodes connection stage. Saves result as regions_graph.p
    :param run: boolean. Whether to run again or load rel. files
    :param theta: int. Angle as theta parallel linking angle
    :param THRESHOLD: int/float. Threshold for correlation coeff. score. Defines if a voxel enters the graph
    :return: Regional graph with best scored voxels as nodes.
    """
    try:
        if run:
            utils.set_status(Messages.START_GRAPH)
            graph = graph_creation(target_map, scores, directions, dic_direct, theta, thresh=THRESHOLD)
            utils.set_status(Messages.END_GRAPH)
            utils.dump(path=source_dir + "regions_graph.p", object=graph)
        else:
            graph = utils.load(path=source_dir + "regions_graph.p")
        return graph
    except Exception as e:
        utils.set_status(Messages.FAIL_GRAPH)
        return None


def run_linkage(run, graph, mid, line, apix):
    """
    Runs Linkage Stage. Saves output as linked_graph
    :param run: boolean. Whether to run again or load rel. files
    :param mid: mid distance thresh.
    :param line: line distance thresh.
    :return: Regional graph, after connecting regions
    """
    try:
        if run:
            utils.set_status(Messages.START_LINK)
            graph2=link_regions(graph, mid, line, apix)
            utils.set_status(Messages.END_LINK)
            utils.dump(path=source_dir + "linked_graph.p", object=graph2)
        else:
            graph2 = utils.load(source_dir + "linked_graph.p")
        return graph2
    except Exception as e:
        utils.set_status(Messages.FAIL_LINK)
        return None


def run_pruning(target_map, run, graph2):
    """
    Runs pruning
    :param run: boolean. Whether to run again or load rel. files
    :return: Regional graph after pruning
    """
    # try:
    if run:
        utils.set_status(Messages.START_PRUN)
        output, graph3 = pruning(graph2, target_map)
        utils.set_status(Messages.END_PRUN)
        utils.dump(path=dir_path + "output", object=output, is_np=True)
        utils.dump(path=source_dir + "graph3.p", object=graph3, is_np=False)

    else:
        output = utils.load(path=source_dir + "output", is_np=True)
        graph3 = utils.load(path=source_dir + "graph3.p", is_np=False)
    return output, graph3
# except Exception as e:
    #     utils.set_status(Messages.FAIL_PRUN)
    #     print e.message
    #     return None


def back_main(thresh, theta, mid, line, start, target_path):
    """
    Go back a stage if a main stage failed
    """
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

    # Create projects directories for intermediate file savings
    create_project_dirs()

    # Read map input file. Get map instance and its apix
    target_map, apix = read_map(input_path=input_path)

    # Generate templates. Get directions vectors
    dic_directions = run_templates(target_path, run=True if start<1 else False)

    # Run correlation. Get man scores and max directions dicts
    max_scores, max_dirs = run_correlation(target_map, run=True if start<2 else False)

    # Run graph creation. Get regional graph with high scored voxels as Nodes
    graph = run_graph(target_map, run=True if start<3 else False, scores=max_scores,directions= max_dirs,dic_direct=dic_directions,
                      theta=theta, THRESHOLD=thresh)
    # Run linkage. Get regional graph after region linking
    graph2 = run_linkage(run=True if start<4 else False, graph=graph, mid=mid, line=line, apix=apix)

    # Run pruning. Get regional graph after bad regions prune
    output, graph3 = run_pruning(target_map=target_map, run=True if start<5 else False, graph2=graph2)

    utils.set_status(Messages.END_RUN.format(len(graph2.regions)))

    # Output resulted mrc file
    output_as_map(graph3, target_map)

    # Plot the result in 3D
    plot_matrix(graph3, target_map.box_size())

if __name__ == "__main__":
    main()