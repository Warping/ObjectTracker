import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import distance
#from target import Target

def compute_velocity(target_pos, detection, dt):
    dx = np.abs(target_pos - detection)
    return np.linalg.norm(dx) / dt

def get_cost_matrix(targets, old_positions, detections, cost_type='dist', dt=None):
    if len(targets) != len(old_positions):
        raise ValueError(f'The amount of targets must be equal to the amount of old positions')

    high_assignment_cost = 100000 # a cost that we will never reach in the scope of this environment
    rows = len(targets)
    cols = len(detections)
    cost_matrix = np.full((rows,cols), fill_value=high_assignment_cost)
    for i, target in enumerate(targets):
        for j, detection in enumerate(detections):
            targ_pos = old_positions[i]
            if cost_type == 'velocity':
                if not isinstance(dt, (int,float)):
                    raise ValueError(f'Cost type is \'velocity\' yet dt is not of type int or float. Got type(dt) = \'{type(dt)}\'.')
                # This creates costs from the normal of the velocity from a previous position to a new position
                # ex the cost between (3,2) and (4,4) = sqrt(5)/dt
                cost_matrix[i,j] = compute_velocity(targ_pos, detection, dt)
            elif cost_type == 'dist':
                # This creates costs based off the total distance between a previous position to a new position
                cost_matrix[i,j] = np.linalg.norm(targ_pos - detection)
    return cost_matrix

def associate_detections(targets, detections, cost_matrix, return_type='list', max_vel=None, max_dist=None, dt=None):
    # TODO: I believe max_vel and max_dist are useless here because the thresholds are checked within
    # the frame handler now. Remove when verified to be useless
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
        akd = {}
        for assoc in associations:
            tg = assoc[0]
            match = assoc[1]
            akd[tg] = match
        return akd
    else:
        return associations

            
def associate(targets, old_positions, detections, return_type='list', cost_type='dist', max_dist=None, max_vel=None, dt=None):
    """
    A wrapper for doing a full Hungarian Algorithm call. `targets` can be anything
    but likely will be the objects that are being referenced and old_positions is likely
    going to be said targets' _ukf.x. If doing association merely on positions

    max_vel is the threshold for the maximum velocity between two positions. If exceeded,
    it will not be considered a match.
    max_dist is similar to max vel but uses euclidean distance instead of velocity.
    """
    if cost_type == 'velocity':
        if not isinstance(dt, (int,float)):
            raise ValueError
    cost_matrix = get_cost_matrix(targets, old_positions, detections, cost_type=cost_type, dt=dt)
    associations = associate_detections(targets, detections, cost_matrix, return_type=return_type, dt=dt)
    return associations

