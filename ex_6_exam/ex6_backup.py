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
min_dodge_thresh = 300
max_dodge_thresh = 1000

# constants
lastSeenLM = None
LMInSight = False
lastMeasuredAngle = 0
translationInOneSecond = 200
rotationInOneSecond = 0.73  # 0.qqaw79 # 1.13826
weightMean = 0
visitedLM = [False, False, False, False]
turn_counter = 0
foundMiddle = False
sigma_distance = 15.0  # chose a number
sigma_theta = 1.0
safety_dist = 40.0
eps = 0.01
forceCheck = False
avoiding_box = False


# Landmarks. Their coordinates are in cm.
landmarks = [(0.0, 0.0), (0.0, 300.0), (400.0, 0.0), (400.0, 300.0)]


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
    lm2 = (int(landmarks[2][0] + offsetX),
           int(ymax - (landmarks[2][1] + offsetY)))
    lm3 = (int(landmarks[3][0] + offsetX),
           int(ymax - (landmarks[3][1] + offsetY)))
    
    cv2.circle(world, lm0, 5, CRED, 2)
    cv2.circle(world, lm1, 5, CGREEN, 2)
    cv2.circle(world, lm2, 5, CBLUE, 2)
    cv2.circle(world, lm3, 5, CYELLOW, 2)
    cv2.putText(world, 'LM 1',lm0, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.putText(world, 'LM 2',lm1, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.putText(world, 'LM 3',lm2, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.putText(world, 'LM 4',lm3, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)




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
world = np.zeros((800, 800, 3), dtype=np.uint8)

# Draw map
draw_world(est_pose, particles, world)

print "Opening and initializing camera"

#cam = camera.Camera(0, 'macbookpro')
#cam = camera.Camera(0, 'frindo')
cam = camera.Camera(0, 'arlo')


def turnToLandmark(angle):
    if angle > 0:
        arlo.go_diff(30, 29, 0, 1)
    elif angle < 0:
        arlo.go_diff(30, 29, 1, 0)
    sleep(abs(angle) / rotationInOneSecond)
    arlo.stop()
    



def driveArlo(t, particles):
    global turn_counter
    turn_counter=0
    actual_driven_dist, current_time, c = 0, 0, 0
    dt = t / 25.0

    while current_time < t:
        a = time.clock()
        current_time += dt + c
        actual_driven_dist += dt * translationInOneSecond

        stop_dist = 300
        sensor_reads = [arlo.read_sensor(
            0), arlo.read_sensor(2), arlo.read_sensor(3)]
        print "Front: {0} - Left: {1} - Right: {2}".format(sensor_reads[0], sensor_reads[1], sensor_reads[2])
        if(sensorStop(sensor_reads, stop_dist)):
            break

        arlo.go_diff(80, 79, 1, 1)
        b = time.clock()
        c = b - a
        sleep(abs(dt - c))
    return actual_driven_dist


def sensorStop(sensor_reads, stop_dist):
    if sensor_reads[0] < stop_dist or sensor_reads[1] < stop_dist or sensor_reads[2] < stop_dist:
        # arlo.stop()
        # arlo.go_diff(80,79,0,0)
        # sleep(0.15)
        arlo.stop()
        MInSight = False
        print "Sensor stopp!"
        return True
    return False


def updateParticles(particles):
    for particle in particles:
        dx = np.cos(particle.getTheta()) * translationInOneSecond
        dy = np.sin(particle.getTheta()) * translationInOneSecond
        par.move_particle(particle, dx, dy, 
                          (math.pi * 0.50) / rotationInOneSecond)

def sampleWeights():
    weight_sum = 0.0
    for particle in particles:
        posWeight = 0
        angleWeight = 0

        calculated_distance = (
            math.sqrt((particle.getX() - lm[0])**2 + ((particle.getY() - lm[1]))**2))

        posWeight = (1 / math.sqrt(2 * math.pi * sigma_distance**2)) * math.exp(-1 *
                                                                                (measured_distance - calculated_distance)**2 / (2 * sigma_distance**2))

        p_theta = particle.getTheta()

        if particle.getY() < 0:
            p_theta = math.pi * 2 - p_theta

        phi = math.acos((lm[0] - particle.getX()) /
                        calculated_distance) - p_theta

        angleWeight = (1 / math.sqrt(2 * math.pi * sigma_theta**2)) * \
            math.exp(-1 * (((measured_angle - phi)**2) / (2 * sigma_theta**2)))

        particle.setWeight(posWeight * angleWeight)
        weight_sum += posWeight * angleWeight

    cumsum = [0.0]
    tsum = 0
    for i in particles:
        w = i.getWeight() / weight_sum
        tsum += w
        cumsum.append(tsum)

    print weight_sum
    weightMean = (weight_sum / len(particles)) * 100

    samples = []
    while len(samples) != len(particles):
        sample = np.random.ranf()
        for i in range(len(cumsum)):
            if sample >= cumsum[i] and sample < cumsum[i + 1]:
                samples.append(copy.deepcopy(particles[i]))

    for i in range(len(particles)):
        particles[i] = samples[i]

    return weightMean


def correct_lm_found_go_straight():
        # Turn towards landmark
        turnToLandmark(lastMeasuredAngle)
        global turn_counter
        turn_counter=0
            # Drive forward

        dist = math.sqrt((landmarks[lastSeenLM][0] - est_pose.getX())
                         ** 2 + (landmarks[lastSeenLM][1] - est_pose.getY())**2)
        print "DIST", dist
        driving_dist = dist - safety_dist

        # I have substracted safety_dist because it otherwise drove too close to the boxes
        t = (driving_dist) / translationInOneSecond

        actdist = driveArlo(t, particles)
        arlo.stop()
        print "Actual dist: ", actdist, " - Total dist: ", driving_dist
        print "Dist diff: ", driving_dist - actdist


        if abs(driving_dist - actdist) < 30:
            visitedLM[lastSeenLM] = True
            
        LMInSight = False
        updateParticles(particles)
    # The purpose of the next function is get closer into the middel of the two boxes. So after the robot have droven
    # half of the distance to the second box, the robot wil drive from its position into the middel of the virtual chart.

def turn_to_search():
#    turn_counter += 1
    print 'Turning around. Number of turns:', turn_counter

    # rotate
    arlo.go_diff(30, 29, 0, 1)
    sleep((math.pi * 0.25) / rotationInOneSecond)
    arlo.stop()
    for particle in particles:
        par.move_particle(particle, 0, 0, -
                          (math.pi * 0.25) / rotationInOneSecond)
    return 1


while True:
    
    action = cv2.waitKey(15)
    if action == ord("q"):
        break
    # Fetch next frame
    colour, distorted = cam.get_colour()

    # Detect objects
    objectType, measured_distance, measured_angle, colourProb = cam.get_object(
        colour)
    if objectType != 'none':
        print "------------------------------------------------------"
        if (objectType == 'vertical'):
            if colourProb[1] < 0.30:
                lm = landmarks[0]
                lastSeenLM = 0
                print 'Landmark 1. Vertical and red'
            else:
                lm = landmarks[1]
                lastSeenLM = 1
                print 'Landmark 2. Vertical and green'
                
        if (objectType == 'horizontal'):
            if colourProb[1] >0.30:
                lm = landmarks[2]
                lastSeenLM = 2
                print 'Landmark 3. Horizontal and green'
            else:
                lm = landmarks[3]
                lastSeenLM = 3
                print 'Landmark 4. Horizontal and red'
     
        print "Colour probabilities = ", colourProb
        print "Measured distance = ", measured_distance
        print "Measured angle = ", measured_angle
#        print "Object type = ", objectType
#        if colourProb[0] <0.30:
#            print 'The box is green'
#        else: 
#            print 'The box is red'
#        if (objectType == 'horizontal'):
#            print "Landmark is horizontal"
#        elif (objectType == 'vertical'):
#            print "Landmark is vertical"
#        else:
#            print "Unknown landmark type"
#            continue


        # Compute particle weights
        # The weight is calculated_distance, only by looking on the relativ distance
        # from calculated_distance(g(x)) and the measured_distance(f(x))
        # We flip the fraction og f(x)/g(x) i case that g(x) < f(x) so we make sure
        # That our weight is set between 0..1.
        # Weight calculated from hint 6 formulaes
        


#        if objectType == 'horizontal':
#            lm = landmarks[0]
#            lastSeenLM = 0
#        else:
#            lm = landmarks[1]
#            lastSeenLM = 1

        LMInSight = True
        lastMeasuredAngle = measured_angle

        weightMean = sampleWeights()

        # Draw detected pattern
        cam.draw_object(colour)

    else:
        LMInSight = False
        # No observation - reset weights to uniform distribution
        for p in particles:
            p.setWeight(1.0 / num_particles)

    par.add_uncertainty(particles, 5, 0.15)

    # The estimate of the robots current pose
    est_pose = par.estimate_pose(particles)

    print "In sight = {0}".format(LMInSight)
    print "Mean weight = {0}".format(weightMean)
    print "Visited lms: ", visitedLM

    # XXX: Make the robot drive   
    if LMInSight and weightMean < 0.6:
        print 'waiting for the mean to increase'
        
    elif weightMean > 0.6 and LMInSight:
        if lastSeenLM ==0 and not visitedLM[0] and not visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
            print 'Driving towards landmark 1'
            correct_lm_found_go_straight()
            
        elif lastSeenLM ==1 and visitedLM[0] and not visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
            print 'Driving towards landmark 2'
            correct_lm_found_go_straight()
            
        elif lastSeenLM ==2 and visitedLM[0] and visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
            print 'Driving towards landmark 3'
            correct_lm_found_go_straight()
            
        elif lastSeenLM ==3 and visitedLM[0] and visitedLM[1] and  visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
            print 'Driving towards landmark 4'
            correct_lm_found_go_straight()
            
        elif lastSeenLM ==3 and visitedLM[0] and visitedLM[1] and visitedLM[2] and visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
            print 'THE MAP IS COMPLETED'
            
        elif turn_counter < 8:
            turn_counter+=turn_to_search()  
            

                
    elif turn_counter < 8:
            turn_counter+=turn_to_search()  
            
    else:
        print 'I DO NOT KNOW WHAT TO DO!!!'
            

            
            
            
#The next couple of lines need to be changed
#elif not LMInSight or (LMInSight and  lastSeenLM ==1 and visitedLM[0]) or (LMInSight and  lastSeenLM ==2 and visitedLM[1]) or (LMInSight and  lastSeenLM ==3 and visitedLM[2]):

        

#        if visitedLM[0] or visitedLM[1]:  # Going around a box. Explore
#
#            print 'Trying to go around a box in front of me'
#            arlo.go_diff(80, 79, 0, 0)
#            sleep(0.25)
#
#            arlo.go_diff(30, 29, 1, 0)
#            sleep((math.pi * 0.30) / rotationInOneSecond)
#
#            driving_dist = 30
#            t = driving_dist / translationInOneSecond
#            stop_dist = 200
#            actdrive = driveArlo(t, particles)
#
#            arlo.stop()
#
#            arlo.go_diff(30, 29, 0, 1)
#            sleep((math.pi * 0.45) / rotationInOneSecond)
#            arlo.stop()
#
#            driving_dist = 70
#            t = driving_dist / translationInOneSecond
#            stop_dist = 200
#            actdist = driveArlo(t, particles)
#            arlo.stop()
#
#            updateParticles(particles)
#            turn_counter = 0

    draw_world(est_pose, particles, world)
    # Show frame
    cv2.imshow(WIN_RF1, colour)

    # Show world
    cv2.imshow(WIN_World, world)
    # sleep(2)

    # Draw map
    draw_world(est_pose, particles, world)

    # Show frame
    cv2.imshow(WIN_RF1, colour)

    # Show world
    cv2.imshow(WIN_World, world)


# Close all windows
cv2.destroyAllWindows()
