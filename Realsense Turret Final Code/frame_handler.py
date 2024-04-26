import sys
sys.path.insert(1,'./association')

import numpy as np
import uuid
import hungarian_association as HA
from target import Target

class PotentialTarget:
    def __init__(self, initial_pos, min_frames=3, max_missed=3):
        self.min_frames = min_frames
        self.max_missed = max_missed
        self.tracked_frames = 1
        self.missed_frames = 0
        self.pos = np.array([initial_pos])
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
            self.invalid_target = True


class FrameHandler:
    def __init__(self):
        self.cur_frame = np.array([[]])
        self.frame_dt = None
        self.potential_targets = []

    def add_frame(self, frame, dt=None):
        if not isinstance(frame, (list, tuple, np.ndarray)):
            raise ValueError("Frame must be a list, tuple, or ndarray.")
        
        if len(self.potential_targets) == 0 and self.cur_frame.size == 0:
            for point in frame:
                self.potential_targets.append(PotentialTarget(point))
        else:
            if dt is not None and not isinstance(dt, (int, float)):
                raise ValueError(f"dt must be a valid number (float or int), received type(dt) = {type(dt)}")
            self.frame_dt = dt
            self.cur_frame = np.array(frame)

    def associate_frames(self, max_dist=None, max_vel=None):
        if self.cur_frame.size == 0 or len(self.potential_targets) == 0:
            return []
        
        pt_positions = [pt.pos[-1] for pt in self.potential_targets]
        associations = HA.associate(self.potential_targets, pt_positions, self.cur_frame, return_type='dict', max_dist=max_dist)
        new_targets = []
        pt_to_remove = []
        unassociated_points = self.cur_frame.copy()

        for pt in self.potential_targets:
            pt_tuple = (pt,)
            associated_pos = associations[pt_tuple]
            if associated_pos is not None:
                if self._is_within_limits(pt, associated_pos, max_dist, max_vel):
                    pt.add_pos(associated_pos)
                    if pt.is_target:
                        new_targets.append(self._convert_to_target(pt))
                        pt_to_remove.append(pt.uid)
                    # Remove associated point from unassociated
                    unassociated_points = np.array([p for p in unassociated_points if not np.array_equal(p, associated_pos)])
                else:
                    pt.no_match()
                    if pt.invalid_target:
                        pt_to_remove.append(pt.uid)
        
        # Cleanup invalid or converted targets
        self.potential_targets = [pt for pt in self.potential_targets if pt.uid not in pt_to_remove]
        # Create new potential targets for unassociated points
        for pos in unassociated_points:
            self.potential_targets.append(PotentialTarget(pos))

        return new_targets

    def _is_within_limits(self, pt, pos, max_dist, max_vel):
        if max_vel is not None:
            velocity = self._compute_velocity(pt.pos[-1], pos, self.frame_dt)
            if velocity >= max_vel:
                return False
        if max_dist is not None:
            distance = np.linalg.norm(pt.pos[-1] - pos)
            if distance > max_dist:
                return False
        return True

    def _compute_velocity(self, prev_pos, new_pos, dt):
        dx = np.abs(prev_pos - new_pos)
        return np.linalg.norm(dx) / dt

    def _convert_to_target(self, potential_target):
        new_target = Target(_uid=potential_target.uid)
        for pos in potential_target.pos:
            new_target.add_pos(pos, dt=self.frame_dt)
        return new_target

# Example usage (commented out for now)
# handler = FrameHandler()
# handler.add_frame([[1, 2], [3, 4]], dt=0.05)
# targets = handler.associate_frames(max_dist=10, max_vel=2)

