import os
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
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))


def run_linkage(theta, mid, line, apix):
    try:
        with open(dir_path + "/source/graph.p", 'rb') as g:
            graph_prev = pickle.load(g)
        graph=link_regions(graph_prev, theta, mid, line, apix)
        with open(dir_path + "/source/graph2.p", 'wb') as f:
            pickle.dump(graph, f)
        return graph
    except IOError:
        return None


def run_graph(theta,apix, THRESHOLD):
    try:
        scores = np.load(dir_path + "/correlation/max_score")
        directions = np.load(dir_path + "/correlation/max_dirs")
        with open(dir_path + "/correlation/dir_directions.p", 'rb') as g:
            dic_direct = pickle.load(g)
        graph = graph_creation(scores, directions, dic_direct, theta,apix, THRESHOLD=THRESHOLD)
        with open(dir_path + "/source/graph.p", 'wb') as f:
            pickle.dump(graph, f)
        return graph
    except IOError:
        return None


def run_templates(target_map, cylinder_map, overwrite):
    # try:
        dic_directions = create_templates(target_map, cylinder_map, overwrite=True)
        return dic_directions
    # except IOError:
    #     return None


def main(thresh, theta, mid, line, start, path):

    #start = 0: all 1:after create template 2:after correlation 3: after graph 4: just plot

    # # read input files
    target_path = path
    #
    cylinder_creation(target_path)
    ideal_cyl = dir_path + "/source/Cylinder.mrc"
    if not os.path.exists(dir_path + "/correlation"):
        os.makedirs(dir_path + "/correlation")
    try:
        target_map = MapParser.readMRC(target_path)
        cylinder_map = MapParser.readMRC(ideal_cyl)
        apix = target_map.apix

    # except Exception as e:
    #     print e
    except:
       print Messages.INPUT_FILES_ERROR

    if start < 1 or not (len(os.listdir(dir_path + "/Templates")) >= 144):
        # generate templates
        dic_directions = run_templates(target_map, cylinder_map, overwrite=True)
    else:
        try:
            with open(dir_path + "/correlation/dir_directions.p") as g:
                dic_directions = pickle.load(g)
        except IOError:
            if start > 0:
                print Messages.BUMPED_BACK
                return main(thresh, theta, mid, line, start-1, path)





    if start < 2 or (not (os.path.isfile(dir_path + "/correlation" + "/max_score"))):
        try:
            # compute correlation
            max_score, max_dirs = correlate(target_map)
        except IOError:
            if start > 0:
                print Messages.BUMPED_BACK
                return main(thresh, theta, mid, line, start-1, path)
    if start < 3:
        graph = run_graph(theta, apix, THRESHOLD=thresh)
    else:
        try:
            with open(dir_path + "/source/graph.p", 'rb') as g:
                graph = pickle.load(g)
        except IOError:
            graph = run_graph(theta,apix, THRESHOLD=thresh)
            if graph == None:
                if start > 0:
                    print Messages.BUMPED_BACK
                    return main(thresh, theta, mid, line, start - 1, path)
                else:
                    return
    if start < 4:
        graph2 = run_linkage(theta, mid, line, apix)
    else:
        try:
            with open(dir_path + "/source/graph2.p", 'rb') as g:
                graph2 = pickle.load(g)
        except IOError:
            graph2 = run_linkage(theta, mid, line, apix)
            if graph2 == None:
                if start > 0:
                    print Messages.BUMPED_BACK
                    return main(thresh, theta, mid, line, start - 1, path)
                else:
                    return
    plot_matrix(graph2, target_map.box_size())

if __name__ == "__main__":
    main()