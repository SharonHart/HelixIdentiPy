"""
Main runfile

command is either:
    1) python helixindentipy.py gui; start the gui
    2) python helixindentipy.py <path_to_target> threshold=<> theta=<> midpoint_distance=<> lin_distance=<> phase=<>

"""

import sys

from gui import main as gui
from main import main as main_go
from messages import Messages


def main():
    # Default parameters
    threshold = None
    theta = 20
    mid = 13
    line = 4
    phase = 0

    if len(sys.argv) < 2:
        print Messages.NOT_ENOUGH_ARGS

    if sys.argv[1] == "gui":
        gui()
    else:
        path = sys.argv[1]

        if len(sys.argv) > 2:
            args = sys.argv[2:]

            for arg in args:
                split = arg.split("=")
                key = split[0]
                value = split[1]
                if key == "threshold":
                    threshold = float(value)
                elif key == "theta":
                    theta = int(value)
                elif key == "mid":
                    mid = float(value)
                elif key == "line":
                    line = float(value)
                elif key == "phase":
                    if value == "start":
                        phase = 0
                    elif value == "after_templates":
                        phase = 1
                    elif value == "after_correlation":
                        phase = 2
                    elif value == "after_graph":
                        phase = 3
                    elif value == "just_plot":
                        phase = 4

        # Run the main loop
        main_go(threshold, theta, mid, line, phase, path)


if __name__ == "__main__":
    main()
