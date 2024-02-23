import depthEstimation as de

class PositionCalc:
    def __init__(self, max_pos_size=20):
        self.pixel_heights = []
        self.depth_points = []
        self.final_depth = None
        MAX_POS_SIZE = max_pos_size
    
    def add_depth_point(self, pixel_h, depth_c):
        self.pixel_heights.append(pixel_h)
        self.depth_points.append(depth_c)
        if len(self.pixel_heights) > self.MAX_POS_SIZE:
            self.pixel_heights.pop(0)
            self.depth_points.pop(0)
    
    
    def clear_depth_points(self):
        self.pixel_heights = []
        self.depth_points = []

    def get_real_depth(self):
        if len(self.pixel_heights) < self.MAX_POS_SIZE:
            return self.final_depth
        self.final_depth = de.get_real_depth(self.pixel_heights, self.depth_points)
        self.clear_depth_points()
        return self.final_depth
    
class MultiTargetDepthEstimator:
    def __init__(self, max_pos_size=20):
        self.position_calcs = []
        self.MAX_POS_SIZE = max_pos_size
    
    def add_depth_point(self, pixel_h, depth_c, target_num):
        if len(self.position_calcs) < target_num:
            self.position_calcs.append(PositionCalc(self.MAX_POS_SIZE))
        self.position_calcs[target_num].add_depth_point(pixel_h, depth_c)

    def add_depth_points(self, pixel_hs, depth_cs):
        for i, (pixel_h, depth_c) in enumerate(zip(pixel_hs, depth_cs)):
            self.add_depth_point(pixel_h, depth_c, i)
    
    def clear_all_targets(self):
        self.position_calcs = []
    
    def get_real_depths(self):
        real_depths = []
        for position_calc in self.position_calcs:
            real_depths.append(position_calc.get_real_depth())
        return real_depths
        