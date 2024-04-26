import sys
sys.path.insert(1,'./association')

import numpy as np
from target import Target
import hungarian_association as HA
import data_tools as dtools
import uuid


cur_frame = np.array([[]])
frame_dt = None

potential_targets = []
potential_target_min_frames = 3
potential_target_max_missed_frames = 3

class PotentialTarget:
    def __init__(self, initial_pos):
        self.min_frames = potential_target_min_frames
        self.max_missed = potential_target_max_missed_frames
        self.tracked_frames = 1
        self.missed_frames = 0
        self.pos = np.array(initial_pos)
        self.is_target = False
        self.invalid_target = False
        self.uid = uuid.uuid4()
    def add_pos(self, pos):
        self.pos = np.vstack((self.pos, pos))
        self.tracked_frames += 1
        self.missed_frames = 0
        if self.tracked_frames >= self.min_frames:
            self.is_target = True
    def no_match(self):
        self.missed_frames += 1
        if self.missed_frames >= self.max_missed:
            self.invalid_target == True


def add_frame(frame, dt=frame_dt):
    global cur_frame
    global frame_dt
    global potential_targets
    if not isinstance(frame, (list,tuple,np.ndarray)):
        raise ValueError

    if len(potential_targets) == 0 and cur_frame.size == 0:
        for point in frame:
            potential_targets.append(PotentialTarget([point]))
    elif len(potential_targets) != 0 and cur_frame.size == 0:
        if not isinstance(dt,(int,float)):
            raise ValueError(f'dt must be a valid number (float or int), recieved type(dt) = {type(dt)}')
        frame_dt = dt
        cur_frame = np.array(frame) # now this current frame is ready to be associated to the previous potential targets
    else: # probably just redundant because it's the same thing as the previous one but delete it later!
        if not isinstance(dt,(int,float)):
            raise ValueError(f'dt must be a valid number (float or int), recieved type(dt) = {type(dt)}')
        frame_dt = dt
        cur_frame = np.array(frame)

    
def associate_frames(max_dist=None, max_vel=None):
    global potential_targets
    
    cf_not_empty = (cur_frame.size != 0)

    if cf_not_empty and len(potential_targets) != 0:
        # try associating potential targets to the current frame
        # use the target's most recent position for associating
        pt_positions = [pt.pos[-1] for pt in potential_targets]
        associations = HA.associate(potential_targets, pt_positions, cur_frame, return_type='dict', max_dist=max_dist)
        ## maybe max_dist here is pointless if we check it here in this function

    
    # For all the points that could potentially be targets, if they are associated
    # in the next n frames, then consider it a target

    # For all potetial targets which were associated with the current frame, add
    # a position to the potential target and, if a real target, create a new Target
    # from the potential target and remove said potential target from the list
    new_targs = []
    pt_to_remove = [] # the potential set to be removed this frame tracked by their uuid
    unassociated_points = cur_frame

    

    
    # add positions to potential targets and if necessary, convert potential targets into real targets
    for pt in potential_targets:
        pt_tup = (pt,)
        if max_vel != None and isinstance(max_vel, (int,float)):
            threshold_check = pt_last_velocity(pt, frame_dt)
            if type(threshold_check) == type(None):
                threshold_check = pt_next_velocity(pt, dt=frame_dt, pos=associations[pt_tup])
            threshold_check = np.all(threshold_check < max_vel)
        elif max_dist != None and isinstance(max_dist, (int,float)):
            threshold_check = pt_dist(pt.pos[-1],associations[pt_tup]) < max_dist
        if contained(pt_tup, associations.keys()) and threshold_check == True:
            pt.add_pos(associations[pt_tup])
            if pt.is_target:
                new_target = get_new_target(points=pt.pos)
                new_targs.append(new_target)
                pt_to_remove.append(pt.uid)
            # since that point was associated, remove it from the unassociated points
            # even if it's already deleted, it won't be there so it will work out
            for i in range(len(unassociated_points)):
                if np.all(np.equal(unassociated_points[i], associations[pt_tup])):
                    unassociated_points = np.delete(unassociated_points, i, axis=0)
                    break
        else:
            pt.no_match()
            if pt.invalid_target:
                pt_to_remove.append(pt.uid)

    # remove any potential targets which have too many frames without a match
    for r_uuid in pt_to_remove:
        for i,pt in enumerate(potential_targets):
            if pt.uid == r_uuid:
                del potential_targets[i]
                break

    # create new potential targets with positions that have no match whatsoever - a new point
    for pos in unassociated_points:
        potential_targets.append(PotentialTarget(pos))

    return new_targs

def pt_next_velocity(pt, dt, pos):
    if len(pt.pos) < 1:
        return None
    dx = abs(pt.pos[-1] - pos)
    vel = dx/dt
    return vel


def pt_last_velocity(pt, dt):
    if len(pt.pos) <= 1:
        return None
    dx = pt.pos[-1] - pt.pos[-2]
    vel = dx/dt
    return vel

def pt_dist(pt, fpos):
    return np.linalg.norm(pt-fpos)

def contained(subarray, main_array):
    for row in main_array:
        if np.array_equal(row, subarray):
            return True
    return False

def get_new_target(points):
    # currently I don't have an implementation for constructing the Target
    # with an initial set of points, so adding them incrementally for now
    targ = Target()
    for pt in points:
        targ.add_pos(pt,dt=frame_dt)
    return targ
