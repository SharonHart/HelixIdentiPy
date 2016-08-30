import os
import sys
from TEMPy.MapParser import *
from create_templates import main as create_templates
from correlation import main as correlate
from messages import Messages
from create_cylinder import cylinder_creation
from graph import graph_creation
from linkage import link_regions
from plot_result import plot_matrix
import pickle
from matplotlib.mlab import PCA


def main():

    if len(sys.argv) < 2: # todo: change to 3 to get resolution as well
        print Messages.NOT_ENOUGH_ARGS

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # read input files
    target_path = sys.argv[1]

    cylinder_creation(target_path)
    ideal_cyl = dir_path + "/source/Cylinder.mrc"

    res = 0
    if len(sys.argv) > 2:
        res = sys.argv[2]

    try:
        target_map = MapParser.readMRC(target_path)
        cylinder_map = MapParser.readMRC(ideal_cyl)

    except Exception as e:
        print e
    #except:
    #    print Messages.INPUT_FILES_ERROR

    # generate templates
    dic_directions = create_templates(target_map, cylinder_map, overwrite=False)

    # compute correlation
    max_score, max_dirs = correlate(target_map)

    graph = graph_creation(max_score, max_dirs, dic_directions)

    # with open(dir_path + "/source/graph.p", 'wb') as f:
    #     pickle.dump(graph, f)
    #
    # with open(dir_path + "/source/graph.p", 'rb') as g:
    #     graph = pickle.load(g)

    graph=link_regions(graph)
    #
    with open(dir_path + "/source/graph2.p", 'wb') as f:
        pickle.dump(graph, f)

    with open(dir_path + "/source/graph2.p", 'rb') as g:
        graph = pickle.load(g)

    plot_matrix(graph, target_map.box_size())

if __name__ == "__main__":
    main()