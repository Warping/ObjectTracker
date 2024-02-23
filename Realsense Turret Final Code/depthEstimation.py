import numpy as np

pixel_heights = []
depth_points = []

MAX_K_SIZE = 100
k_final = []

def estimate(pixel_h, depth_c):
    k = []
    for h, d in enumerate(pixel_h, depth_c):
        k.append(h*d)
    k_avg = np.mean(k)
    global k_final
    k_final.append(k_avg)
    if len(k_final) > 100:
        k_final.pop(0)
    return 

# Gets the real depth of the target from list of pixel heights and depth values
def get_real_depth(pixel_h, depth_c, resolution=0.1):
    if np.std(depth_c) < resolution:
        estimate(pixel_h, depth_c)
        return depth_c[-1]
    elif len(k_final) != 0:
        depths = []
        global k_final
        k = np.mean(k_final)
        for h in pixel_h:
            depths.append(k/h)
        if np.std(depths) < resolution:
            return np.mean(depths)
        else:
            return None
    else:
        return None