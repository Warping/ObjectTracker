import cv2
from realsense_depth import *
from camera_view import *
from simulation_view import *


cap = DepthCamera((640, 480), (640, 480), 15, 15)
detector = PersonDetector(cap, 'cuda')
simulator = TargetViewer()

while True:
    camera_frame, positions = detector.detect()
    simulator.clearPositions()
    for position in positions:
        simulator.addPosition(position)
    simulator_view = simulator.draw()
    cv2.imshow("Camera", camera_frame)
    cv2.imshow("Simulation", simulator_view)
    if cv2.waitKey(1) == ord('q'):
        break