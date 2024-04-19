import sys
sys.path.insert(1,'./association')

import numpy as np
from target import Target
import hungarian_association as HA
import data_tools as dtools
import uuid


gpts = {'t0':np.array([]),'t':np.array([])}
frame_dt = None

potential_targets = []
potential_target_min_frames = 3

class PotentialTarget:
    def __init__(self, initial_pos):
        self.min_frames = potential_target_min_frames
        self.tracked_frames = 0
        self.pos = np.array(initial_pos)
        self.is_target = False
    def add_pos(self, pos):
        self.pos = np.vstack((self.pos, pos))
        self.tracked_frames += 1
        if self.tracked_frames >= self.min_frames:
            self.is_target = True


def add_frame(frame, dt=frame_dt):
    global gpts
    global frame_dt
    global potential_targets
    if not isinstance(frame, (list,tuple,np.ndarray)):
        raise ValueError
    if gpts['t0'].size == 0 and gpts['t'].size == 0:
        gpts['t0'] = np.array(frame)
        potential_targets = np.array(frame)
    elif gpts['t0'].size != 0 and gpts['t'].size == 0:
        if not isinstance(dt,(int,float)):
            raise ValueError(f'dt must be a valid number (float or int), recieved type(dt) = {type(dt)}')
        gpts['t'] = np.array(frame)
        frame_dt = dt
    else:
        if not isinstance(dt,(int,float)):
            raise ValueError(f'dt must be a valid number (float or int), recieved type(dt) = {type(dt)}')
        gpts['t0'] = gpts['t']
        gpts['t'] = np.array(frame)
        frame_dt = dt

def associate_old_frames():
    global potential_targets
    pt_indices = [i for i in range(len(potential_targets))]
    if gpts['t'].size != 0 and gpts['t0'].size != 0:
        associations = HA.associate(gpts['t0'], gpts['t0'], gpts['t'], return_type='dict')
    else:
        raise Exception('There have not been at least two recorded frames in gpts')
    new_targs = []



    # For all the points that could potentially be targets, if they are associated
    # in the next n frames, then consider it a target
    for pt in potential_targets:
        if contained(pt, associations.keys()):
            new_target = get_new_target(points=[pt, associations[pt]])
            new_targs.append(new_target)
    potential_targets = []
    for pt in gpts['t']:
        if contained(pt, associations.values()):
            potential_targets.append(pt)
    return new_targs


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
