import os
import sys
from TEMPy.MapParser import *
from create_templates import main as create_templates
from correlation import main as correlate
from messages import Messages
from create_cylinder import cylinder_creation


def main():

    if len(sys.argv) < 2: # todo: change to 3 to get resolution as well
        print Messages.NOT_ENOUGH_ARGS

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # read input files
    target_path = sys.argv[1]

    cylinder_creation(target_path);
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
    create_templates(target_map, cylinder_map)

    # compute correlation
    max_score, max_dirs = correlate(target_map)


if __name__ == "__main__":
    main()