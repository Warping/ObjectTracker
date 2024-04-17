import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import distance
#from target import Target

def get_cost_matrix(targets, old_positions, detections):
    if len(targets) != len(old_positions):
        raise ValueError(f'The amount of targets must be equal to the amount of old positions')
    cost_matrix = np.zeros((len(targets), len(detections)))
    for i, target in enumerate(targets):
        for j, detection in enumerate(detections):
            targ_pos = old_positions[i]
            cost_matrix[i,j] = np.linalg.norm(targ_pos - detection)
    return cost_matrix

def associate_detections(targets, detections, cost_matrix, return_type='list'):
    row, col = linear_sum_assignment(cost_matrix)

    if return_type == 'dict':
        associations = {}
        for r,c in zip(row,col):
             associations[targets[r]] = detections[c]
        return associations

    else: #default case, list
        associations = []
        for r,c in zip(row, col):
            associations.append((targets[r],detections[c]))
        return associations
    
def associate(targets, old_positions, detections):
    """
    A wrapper for doing a full Hungarian Algorithm call. `targets` can be anything
    but likely will be the objects that are being referenced and old_positions is likely
    going to be said targets' _ukf.x. If doing association merely on positions
    """
    cost_matrix = get_cost_matrix(targets, old_positions, detections)
    associations = associate_detections(targets, detections, cost_matrix)
    return associations

