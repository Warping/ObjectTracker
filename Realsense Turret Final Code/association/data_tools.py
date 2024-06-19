import numpy as np
import os

def midpoint(p1, p2):
    midp = []
    for ax1,ax2 in zip(p1,p2):
        midp.append((ax1+ax2)/2)
    return np.array(midp)


def record_to_file(path, pos_data, overwrite=False):
    """
    Writes a numpy file to a file specified in `path`.
    The contents will contain either centroid data or box data.
    Ensure that what is written to the file is consistent with future use and testing.
    pos_data shall be a numpy array or similar numpy type
    The file will not be suffixed with .npy at the end of it and must be included in `path`.
    """
    if os.path.exists(path) is False:
        np.save(path, pos_data)
        return 1
    else:
        if overwrite == True:
            np.save(path, pos_data)
            return 1
        else:
            return 0


def load_datafile(path):
    """
    Loads a numpy file from `path` and returns it as an array or -1 
    if the file does not exist.
    """
    if os.path.exists(path):
        dataset = np.load(path)
        return dataset
    else:
        return -1

    






