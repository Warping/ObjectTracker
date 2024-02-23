# Object Tracker
A tracker with the ability to predict the path of a ground based target

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

# Features to Add
Multiple object path prediction
Ability to account for variation in target position and velocity changes at large distances
Implement weighted polyfit for path prediction
