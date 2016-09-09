"""
Project's Utilities.
"""

from __future__ import print_function

import pickle
import numpy as np

import global_vars

def dump(path, object, is_np=False):
    """
    Write to filesystem, an object, to numpy or pickle format file
    :param path: output path
    :param object: object to write
    :param is_np: is a numpy object. otherwise write to pickle
    """
    if not is_np:
        with open(path, 'wb') as f:
            pickle.dump(object, f)
    else:
        with open(path, 'w+') as f:
            np.save(f, object)


def load(path, is_np=False):
    """
    Load a file from filesystem
    :param path: input path
    :param is_np: is numpy object. Otherwise pickle
    :return: The requested object
    """
    if not is_np:
        with open(path, 'rb') as g:
            return pickle.load(g)
    else:
        with open(path, 'r+') as g:
            return np.load(g)


def set_status(stat, same_line=False):
    """
    :param stat: String. Output message
    :param same_line: boolean. print in the same line or not
    """
    if global_vars.isGui:
        global_vars.status_bar.set(stat)
    else:
        if same_line:
            print("\r"+stat, end=" ")
        else:
            print(stat)
