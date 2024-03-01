import numpy as np

pixel_heights = []
depth_points = []

MAX_K_SIZE = 100
k_final = []

def estimate(pixel_h, depth_c):
    """
    Estimates a new value for k_final and appends it
    to the current k_final list. Will maintain MAX_K_SIZE
    and remove the oldest value in k_final if the size of k_final
    is MAX_K_SIZE.
    """
    global k_final
    k = []
    for h, d in enumerate(pixel_h, depth_c):
        k.append(h*d)
    k_avg = np.mean(k)
    k_final.append(k_avg)
    if len(k_final) > 100:
        k_final.pop(0)
    return 


def get_real_depth(pixel_h, depth_c, resolution=0.1):
    """
    This gets the depth of an object with an error within the value
    of resolution. Using the values in k_final, it calculates the depth
    of an object and returns a number for distance.
    """
    global k_final
    if np.std(depth_c) < resolution:
        estimate(pixel_h, depth_c)
        return np.mean(depth_c)
    elif len(k_final) != 0:
        depths = []
        k = np.mean(k_final)
        for h in pixel_h:
            depths.append(k/h)
        if np.std(depths) < resolution:
            return np.mean(depths)
        else:
            return None
    else:
        return None
