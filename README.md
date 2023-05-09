# AutoTurret
A simple turret with the ability to predict the path of a ground based target

# Algorithm
The algorithm used takes into account the positions of a target and calculates 
the speeds and accelerations for each point and uses those to determine if the 
taregt is on a parabolic path. If the target is on a parabolic path, the agorithm 
calculates the required lead angle necessary to hit the target and gives the time
it will take to hit the target. When the target is not on a parabolic path the algorithm
follows the target and leads the target based on the most recent velocity. This ensures
that the angle of the turret is close any future angles calculated by the algorithm
later on.

# Adjustable Parameters
\nTarget and Projectile Speed
\nTarget Acceleration
Target and Turret Position
Number of turrets

# Features to Add
Multiple Target selection
Adjustable effective firing radius
Ability to account for variation in target position and velocity changes at large distances
