import numpy as np

pixel_heights = []
depth_points = []

MAX_K_SIZE = 100
k_final = []


# Constants for the camera. We're using an OAK-D Lite(s) for the project
#
# The FOV is in degrees converted to radians - works better with numpy
CAMERA_DFOV = np.deg2rad(86)
CAMERA_HFOV = np.deg2rad(73)
CAMERA_VFOV = np.deg2rad(58)

# Horizontal distance between the two cameras in millimeters
CAMERA_DISTANCE = 150

# Horizontal width of the cameras in pixels
CAMERA_WIDTH = 480


def estimate(pixel_h, depth_c):
    """
    Estimates a new value for k_final and appends it
    to the current k_final list. Will maintain MAX_K_SIZE
    and remove the oldest value in k_final if the size of k_final
    is MAX_K_SIZE.
    """
    global k_final
    k = []
    for h, d in zip(pixel_h, depth_c):
        k.append(h*d)
    k_avg = np.mean(k)
    k_final.append(k_avg)
    if len(k_final) > MAX_K_SIZE:
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
        return depth_c[-1]
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

def stereo_depth(x_1, x_2):
    D = (CAMERA_DISTANCE * CAMERA_WIDTH)/(2 * np.tan(CAMERA_HFOV / 2) * (x_1 - x_2))
    return D
