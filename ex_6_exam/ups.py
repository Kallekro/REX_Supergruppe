from __future__ import division
import cv2
import particle as par
import camera
import numpy as np
import math
import random_numbers as r
import copy
import robot
from time import sleep
import time

# TODO: The coordinate system is such that the y-axis points downwards due to the visualization in draw_world.
# Consider changing the coordinate system into a normal cartesian coordinate system.

# Some colors constants
CRED = (0, 0, 255)
CGREEN = (0, 255, 0)
CBLUE = (255, 0, 0)
CCYAN = (255, 255, 0)
CYELLOW = (0, 255, 255)
CMAGENTA = (255, 0, 255)
CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)

# constants
lastMeasuredAngle = 0
translationInOneSecond = 200
rotationInOneSecond = 0.73  # 0.qqaw79 # 1.13826
min_dodge_thresh = 300
max_dodge_thresh = 1000

#variables
lastSeenLM = None
LMInSight = False
weightMean = 0
visitedLM = [False, False, False, False]
turn_counter = 0
foundMiddle = False
sigma_distance = 15.0  # chose a number
sigma_theta = 1.0
safety_dist = 40.0
eps = 0.01
next_lm = 1
forceCheck = False
avoiding_box = False

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in cm.
landmarks = [(0.0, 0.0), (200.0, 0.0)]


def deltaX(Theta, DrivenDistance):
    return np.cos(Theta * 180 / np.pi) * DrivenDistance


def deltaY(Theta, DrivenDistance):
    return np.sin(Theta * 180 / np.pi) * DrivenDistance


def jet(x):
    """Colour map for drawing particles. This function determines the colour of
    a particle from its weight."""
    r = (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (4.0 * x - 3.0 / 2.0) + (x >=
                                                                      5.0 / 8.0 and x < 7.0 / 8.0) + (x >= 7.0 / 8.0) * (-4.0 * x + 9.0 / 2.0)
    g = (x >= 1.0 / 8.0 and x < 3.0 / 8.0) * (4.0 * x - 1.0 / 2.0) + (x >= 3.0 /
                                                                      8.0 and x < 5.0 / 8.0) + (x >= 5.0 / 8.0 and x < 7.0 / 8.0) * (-4.0 * x + 7.0 / 2.0)
    b = (x < 1.0 / 8.0) * (4.0 * x + 1.0 / 2.0) + (x >= 1.0 / 8.0 and x <
                                                   3.0 / 8.0) + (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (-4.0 * x + 5.0 / 2.0)

    return (255.0 * r, 255.0 * g, 255.0 * b)


def draw_world(est_pose, particles, world):
    """Visualization.
    This functions draws robots position in the world coordinate system."""

    # Fix the origin of the coordinate system
    offsetX = 100
    offsetY = 250

    # Constant needed for transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]

    world[:] = CWHITE  # Clear background to white

    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX()) + offsetX
        y = ymax - (int(particle.getY()) + offsetY)
        colour = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x, y), 2, colour, 2)
        b = (int(particle.getX() + 15.0 * np.cos(particle.getTheta())) + offsetX,
             ymax - (int(particle.getY() - 15.0 * np.sin(particle.getTheta())) + offsetY))
        cv2.line(world, (x, y), b, colour, 2)

    # Draw landmarks
    lm0 = (int(landmarks[0][0] + offsetX),
           int(ymax - (landmarks[0][1] + offsetY)))
    lm1 = (int(landmarks[1][0] + offsetX),
           int(ymax - (landmarks[1][1] + offsetY)))
    cv2.circle(world, lm0, 5, CRED, 2)
    cv2.circle(world, lm1, 5, CGREEN, 2)

    # Draw estimated robot pose
    a = (int(est_pose.getX()) + offsetX, ymax - (int(est_pose.getY()) + offsetY))
    b = (int(est_pose.getX() + 15.0 * np.cos(est_pose.getTheta())) + offsetX,
         ymax - (int(est_pose.getY() - 15.0 * np.sin(est_pose.getTheta())) + offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)


### Main program ###

# Open windows
WIN_RF1 = "Robot view"
cv2.namedWindow(WIN_RF1)
cv2.moveWindow(WIN_RF1, 50, 50)

WIN_World = "World view"
cv2.namedWindow(WIN_World)
cv2.moveWindow(WIN_World, 500, 50)


# Initialize particles
num_particles = 250
particles = []
for i in range(num_particles):
    # Random starting points. (x,y) \in [-1000, 1000]^2, theta \in [-pi, pi].
    p = par.Particle(2000.0 * np.random.ranf() - 1000, 2000.0 * np.random.ranf() -
                     1000, 2.0 * np.pi * np.random.ranf() - np.pi, 1.0 / num_particles)
    #p = particle.Particle(2000.0*np.random.ranf() - 1000, 2000.0*np.random.ranf() - 1000, np.pi+3.0*np.pi/4.0, 1.0/num_particles)
    particles.append(p)

# The estimate of the robots current pose
est_pose = par.estimate_pose(particles)

# Driving parameters
velocity = 0.0  # cm/sec
angular_velocity = 0.0  # radians/sec

# Initialize the robot (XXX: You do this)
arlo = robot.Robot()


# Allocate space for world map
world = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw map
draw_world(est_pose, particles, world)

print "Opening and initializing camera"

#cam = camera.Camera(0, 'macbookpro')
#cam = camera.Camera(0, 'frindo')
cam = camera.Camera(0, 'arlo')


def turnAngle(angle):
    if angle > 0:
        arlo.go_diff(30, 29, 0, 1)
    elif angle < 0:
        arlo.go_diff(30, 29, 1, 0)
    sleep(abs(angle) / rotationInOneSecond)
    arlo.stop()


