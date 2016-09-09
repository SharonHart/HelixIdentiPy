import pickle
import numpy as np

import global_vars


def dump(path, object, is_np=False):
    if not is_np:
        with open(path, 'wb') as f:
            pickle.dump(object, f)
    else:
        with open(path, 'w+') as f:
            np.save(f, object)


def load(path, is_np=False):
    if not is_np:
        with open(path, 'rb') as g:
            return pickle.load(g)
    else:
        with open(path, 'r+') as g:
            return np.load(g)


def set_status(stat):
    if global_vars.isGui:
        global_vars.status_bar.set(stat)
    else:
        print stat
