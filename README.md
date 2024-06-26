# Object Tracker
A tracker with the ability to predict the path of a ground based target

# Note
This public branch does not contain the specific implementation of our finalized algorithm and 
ONLY contains the publicly available pieces needed for a full implementation. A short video of the
prototype in action can be viewed here:

https://youtube.com/shorts/yPidxpDLN4A?si=5Ecqifw0415ue5ss

https://youtu.be/BcbsO29NmmU?si=AnJfAcd7cHpyQWCG

https://youtu.be/3YItegcZnLA?si=GTx35yHF8zh_ZAJA

# Projection Algorithm
The algorithm for the de-projection of the 2d image involves grabbing a depth map 
of the current camera frame and AI to find the object we want the depth of. The
algorithm then takes the depth value and pixel positions to calculate the 3d point in
space. We can then track this point over time for path prediction

# Prediction Algorithm
The algorithm used takes into account the positions of a target and calculates 
the speeds and accelerations for each point and uses those to determine if the 
taregt is on a parabolic path. If the target is on a parabolic path, the agorithm 
calculates the required lead angle necessary to hit the target and gives the time
it will take to hit the target. When the target is not on a parabolic path the algorithm
follows the target and leads the target based on the most recent velocity. This ensures
that the angle of the turret is close any future angles calculated by the algorithm
later on.

# Adjustable Parameters
Number of MAX tracked object

Number of points to graph

Resolution of depth tracking

Precision of Inference Model

# Human Tracking Specifics
Uses YOLOv8-pose to perform high quality tracking in a 2D image (Eliminates false positives)

Creates bounding box from pose points to create region for lidar scanning to calibrate depth

Calibration allows system to use height of person to track their depth when lidar error is high

# Features to Add
Multiple object path prediction (Implemented)

Ability to distinguish objects from one another using an ID system. (Implemented)

Ability to account for variation in target position and velocity changes at large distances (Implemented)

Implement weighted polyfit for path prediction

Implement stereo image disparity based depth tracking as opposed to using apparent height
