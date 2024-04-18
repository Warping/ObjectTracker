import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import distance
#from target import Target

def get_cost_matrix(targets, old_positions, detections):
    if len(targets) != len(old_positions):
        raise ValueError(f'The amount of targets must be equal to the amount of old positions')

    high_assignment_cost = 10000 # a cost that we will never reach in the scope of this product
    rows = len(targets)
    cols = len(detections)
    cost_matrix = np.full((rows,cols), fill_value=high_assignment_cost)
    for i, target in enumerate(targets):
        for j, detection in enumerate(detections):
            targ_pos = old_positions[i]
            cost_matrix[i,j] = np.linalg.norm(targ_pos - detection)
    return cost_matrix

def associate_detections(targets, detections, cost_matrix, return_type='list'):
    row, col = linear_sum_assignment(cost_matrix)

    num_targets = len(targets)
    num_detections = len(detections)
    associations = []

    if num_targets > num_detections:
        for r in range(num_targets):
            min_cost_index = np.argmin(cost_matrix[r, :num_detections])
            associations.append((targets[r], detections[min_cost_index]))
    else:
        for r,c in zip(row,col):
            if c < num_detections and r < num_targets:
                associations.append((targets[r],detections[c]))


         

    if return_type == 'dict':
        assoc_dict = {}
        names = [n[0] for n in associations]
        match = [n[1] for n in associations]
        for n,m in zip(names,match):
            assoc_dict[n] = m
        return assoc_dict
    else:
        return associations

            
def associate(targets, old_positions, detections, return_type='list'):
    """
    A wrapper for doing a full Hungarian Algorithm call. `targets` can be anything
    but likely will be the objects that are being referenced and old_positions is likely
    going to be said targets' _ukf.x. If doing association merely on positions
    """
    cost_matrix = get_cost_matrix(targets, old_positions, detections)
    associations = associate_detections(targets, detections, cost_matrix, return_type=return_type)
    return associations

