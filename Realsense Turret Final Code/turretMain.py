import cv2
from realsense_depth import *
from camera_view import *
from simulation_view import *
import position_calc as pc
import depthai_depth as dd
import CONFIG

# Prepare CONFIG for use across all other modules
CONFIG.setup_config()
conf = CONFIG.config

#CAP_RES = (1280, 720)
CAP_RES = (conf['Camera']['width'], conf['Camera']['height'])
SIM_RES = (640, 480)


if __name__ == '__main__':
    # cap = DepthCamera(CAP_RES, 30, 30)
    cap = dd.OakDepthCam(CAP_RES, 30, 30)
    detector = PersonDetector(cap, conf['YOLO']['Architecture'])
    simulator = TargetViewer(SIM_RES)
    mtde = pc.MultiTargetDepthEstimator(5)
    while True:
        start_time = time()

        detector.update()
        # depths will be an array of depths at time t for n targets (depths[n] = depth of target n)
        # heights will be an array of heights at time t for n targets (heights[n] = height of target n)
        # centers will be an array of center points at time t for n targets (centers[n] = center of target n)
        depths, heights, centers = detector.getDHCPerTarget()

        # Get real depths of targets
        new_depths = []
        if (len(mtde.position_calcs) != len(depths)):
            mtde.clear_all_targets()
        print("depths: ", depths)
        print("heights: ", heights)
        mtde.add_depth_points(heights, depths)
        real_depths = mtde.get_real_depths()
        for depth, real_depth in zip(depths, real_depths):
            if real_depth is not None:
                new_depths.append(real_depth)
            else:
                new_depths.append(depth)
    
        # Get the final frame from the camera
        # Get the positions of the targets in 3D space
        positions = detector.getTargetPositions(new_depths, centers)
        simulator.clearPositions()
        for position in positions:
            simulator.addPosition(position)
        simulator_view = simulator.draw()
        camera_frame = detector.getFinalFrame(new_depths, heights, centers, start_time)
        cv2.imshow("Camera", camera_frame)
        cv2.imshow("Simulation", simulator_view)
        if cv2.waitKey(1) == ord('q'):
        break
