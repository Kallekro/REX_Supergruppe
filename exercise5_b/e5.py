from __future__ import division
import cv2
import particle as par
import camera
import numpy as np
import math
import random_numbers as rnd
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

sigma_distance= 15.0 # chose a number
sigma_theta=1.0

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in cm.
landmarks = [(0.0, 0.0), (200.0, 0.0)]

def deltaX(Theta,DrivenDistance):
	return np.cos(Theta*180/np.pi)*DrivenDistance

def deltaY(Theta,DrivenDistance):
	return np.sin(Theta*180/np.pi)*DrivenDistance

def jet(x):
    """Colour map for drawing particles. This function determines the colour of 
    a particle from its weight."""
    r = (x >= 3.0/8.0 and x < 5.0/8.0) * (4.0 * x - 3.0/2.0) + (x >= 5.0/8.0 and x < 7.0/8.0) + (x >= 7.0/8.0) * (-4.0 * x + 9.0/2.0)
    g = (x >= 1.0/8.0 and x < 3.0/8.0) * (4.0 * x - 1.0/2.0) + (x >= 3.0/8.0 and x < 5.0/8.0) + (x >= 5.0/8.0 and x < 7.0/8.0) * (-4.0 * x + 7.0/2.0)
    b = (x < 1.0/8.0) * (4.0 * x + 1.0/2.0) + (x >= 1.0/8.0 and x < 3.0/8.0) + (x >= 3.0/8.0 and x < 5.0/8.0) * (-4.0 * x + 5.0/2.0)

    return (255.0*r, 255.0*g, 255.0*b)

def draw_world(est_pose, particles, world):
    """Visualization.
    This functions draws robots position in the world coordinate system."""
        
    # Fix the origin of the coordinate system
    offsetX = 100;
    offsetY = 250;
    
    # Constant needed for transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]
    
    world[:] = CWHITE # Clear background to white
    
    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX()) + offsetX
        y = ymax - (int(particle.getY()) + offsetY)
        colour = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x,y), 2, colour, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX, 
                                     ymax - (int(particle.getY() - 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x,y), b, colour, 2)
   
    # Draw landmarks
    lm0 = (int(landmarks[0][0]+offsetX), int(ymax-(landmarks[0][1]+offsetY)))
    lm1 = (int(landmarks[1][0]+offsetX), int(ymax-(landmarks[1][1]+offsetY)))
    cv2.circle(world, lm0, 5, CRED, 2)
    cv2.circle(world, lm1, 5, CGREEN, 2)
    
    # Draw estimated robot pose
    a = (int(est_pose.getX())+offsetX, ymax-(int(est_pose.getY())+offsetY))
    b = (int(est_pose.getX() + 15.0*np.cos(est_pose.getTheta()))+offsetX, 
                                 ymax-(int(est_pose.getY() - 15.0*np.sin(est_pose.getTheta()))+offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)


### Main program ###

# Open windows
WIN_RF1 = "Robot view";
cv2.namedWindow(WIN_RF1);
cv2.moveWindow(WIN_RF1, 50       , 50);

WIN_World = "World view";
cv2.namedWindow(WIN_World);
cv2.moveWindow(WIN_World, 500       , 50);


# Initialize particles
num_particles = 250 
particles = []
for i in range(num_particles):
    # Random starting points. (x,y) \in [-1000, 1000]^2, theta \in [-pi, pi].
    p = par.Particle(2000.0*np.random.ranf() - 1000, 2000.0*np.random.ranf() - 1000, 2.0*np.pi*np.random.ranf() - np.pi, 1.0/num_particles)
    #p = particle.Particle(2000.0*np.random.ranf() - 1000, 2000.0*np.random.ranf() - 1000, np.pi+3.0*np.pi/4.0, 1.0/num_particles)
    particles.append(p)

est_pose = par.estimate_pose(particles) # The estimate of the robots current pose

# Driving parameters
velocity = 0.0; # cm/sec
angular_velocity = 0.0; # radians/sec

# Initialize the robot (XXX: You do this)
arlo = robot.Robot()
lastSeenLM = None
LMInSight = False
lastMeasuredAngle = 0
translationInOneSecond = 100 
rotationInOneSecond = 0.73 #0.qqaw79 # 1.13826 
weightMean = 0
visitedLM = [False, False]
turn_counter = 0

# Allocate space for world map
world = np.zeros((500,500,3), dtype=np.uint8)

# Draw map
draw_world(est_pose, particles, world)

print "Opening and initializing camera"

#cam = camera.Camera(0, 'macbookpro')
#cam = camera.Camera(0, 'frindo')
cam = camera.Camera(0, 'arlo')

while True:
    #if visitedLM[0] and visitedLM[1]:
    #  # VICTORY
    #  arlo.go_diff(80, 79, 1, 0)
    #  sleep(2)
    #  arlo.stop()
    #  while cv2.waitKey(15) != ord('q'):
    #    continue 
    #  break
    # Move the robot according to user input (for testing)
    action = cv2.waitKey(15)
    
    if action == ord('w'): # Forward
        velocity += 4.0;
    elif action == ord('x'): # Backwards
        velocity -= 4.0;
    elif action == ord('s'): # Stop
        velocity = 0.0;
        angular_velocity = 0.0;
    elif action == ord('a'): # Left
        angular_velocity -= 0.2;
    elif action == ord('d'): # Right
        angular_velocity += 0.2;
    elif action == ord('q'): # Quit
        break
    elif action == ord('g'): # GO
        arlo_go = True
    else:
        arlo_go = False

        
    # Read odometry, see how far we have moved, and update particles.
    # Or use motor controls to update particles
    # XXX: You do this

    # Fetch next frame
    colour, distorted = cam.get_colour()    
    
    # Detect objects
    objectType, measured_distance, measured_angle, colourProb = cam.get_object(colour)
    if objectType != 'none':
        print "Object type = ", objectType
        print "Measured distance = ", measured_distance
        print "Measured angle = ", measured_angle
        print "Colour probabilities = ", colourProb

        if (objectType == 'horizontal'):
            print "Landmark is horizontal"
        elif (objectType == 'vertical'):
            print "Landmark is vertical"
        else:
            print "Unknown landmark type"
            continue

        # Compute particle weights
        # The weight is calculated_distance, only by looking on the relativ distance
        # from calculated_distance(g(x)) and the measured_distance(f(x))
        # We flip the fraction og f(x)/g(x) i case that g(x) < f(x) so we make sure
        # That our weight is set between 0..1.
        # When the landmark is vertical, it means that we look on the landmark
        # with the pos (300,0), therefore we need to subtrac 300, from the particles
        # That is over there, to get the true distance from the landmark!!!!
        #Weight calculated from hint 6 formulaes

        if objectType == 'horizontal':
            lm = landmarks[0]
            lastSeenLM = 0
        else:
            lm = landmarks[1]
            lastSeenLM = 1

        LMInSight = True
        lastMeasuredAngle = measured_angle

        weight_sum = 0.0
        for particle in particles:
           posWeight = 0;
           angleWeight = 0;

           calculated_distance = (math.sqrt((particle.getX()-lm[0])**2 + ((particle.getY()-lm[1]))**2))

           posWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_distance-calculated_distance)**2/(2*sigma_distance**2))

           p_theta = particle.getTheta()

           if particle.getY() < 0:
               p_theta = math.pi*2 - p_theta
           
           phi = math.acos(( lm[0] - particle.getX() ) / calculated_distance) - p_theta
           
           angleWeight = (1/math.sqrt(2*math.pi*sigma_theta**2))*math.exp(-1* (((measured_angle-phi)**2)/(2*sigma_theta**2)))

           particle.setWeight(posWeight*angleWeight)
           weight_sum += posWeight*angleWeight            

        cumsum = [0.0]
        tsum = 0
        for i in particles:
            w = i.getWeight() / weight_sum
            tsum += w
            cumsum.append(tsum)

        print weight_sum
        weightMean = (weight_sum / len(particles)) * 100  

        samples = []
        #resample_n = 1000
        while len(samples) != len(particles):
            sample = np.random.ranf()
            for i in range(len(cumsum)):
                if sample >= cumsum[i] and sample < cumsum[i+1]:
                    samples.append(copy.deepcopy(particles[i]))

        for i in range(len(particles)):
            particles[i] = samples[i]
            
        
        # Draw detected pattern
        cam.draw_object(colour)

    else:
        LMInSight = False
        # No observation - reset weights to uniform distribution
        for p in particles:
            p.setWeight(1.0/num_particles)

    par.add_uncertainty(particles, 5, 0.15)

    
    est_pose = par.estimate_pose(particles) # The estimate of the robots current pose

    print "In sight = {0}".format(LMInSight)
    print "Mean weight = {0}".format(weightMean) 
    print "Visited lms: ", visitedLM

    # XXX: Make the robot drive
    if weightMean > 0.6 and LMInSight and not visitedLM[lastSeenLM]:
        turn_counter = 0
        # Turn towards landmark
        if lastMeasuredAngle > 0:
            arlo.go_diff(30, 29, 0, 1)
        elif lastMeasuredAngle < 0:
            arlo.go_diff(30, 29, 1, 0)

        eps = 0.1
        if lastMeasuredAngle < 0-eps or lastMeasuredAngle > 0+eps:
            sleep((abs(lastMeasuredAngle)) / rotationInOneSecond)
            arlo.stop()

        # Drive forward
        safety_dist=40.0
        dist = math.sqrt((landmarks[lastSeenLM][0] - est_pose.getX())**2 + (landmarks[lastSeenLM][1] - est_pose.getY())**2) 
        driving_dist = dist - safety_dist# - 35
        if visitedLM[0] or visitedLM[1]:
            driving_dist /= 2
        
        actual_driven_dist = 0  
        t = (driving_dist)/translationInOneSecond #I have substracted safety_dist because it otherwise drove too close to the boxes
        dt = t/25.0 
        current_time = 0
        c = 0
        while current_time < t:
            a = time.clock()
            current_time += dt+c
            actual_driven_dist += dt*translationInOneSecond 
            
            stop_dist = 300
            sensor_reads = [arlo.read_sensor(0), arlo.read_sensor(2), arlo.read_sensor(3)]
            print "Front: {0} - Left: {1} - Right: {2}".format(sensor_reads[0], sensor_reads[1], sensor_reads[2])
            if sensor_reads[0] < stop_dist or sensor_reads[1] < stop_dist or sensor_reads[2] < stop_dist: 
                arlo.stop()
                LMInSight = False
                print "Sensor stopp!"
                break
          
            arlo.go_diff(80, 79, 1, 1)
            b = time.clock()
            c = b-a
            sleep((dt-c))
        arlo.stop()
        print "Front: {0} - Left: {1} - Right: {2}".format(sensor_reads[0], sensor_reads[1], sensor_reads[2])

        print "Actual dist: ", actual_driven_dist, " - Total dist: ", driving_dist
        print "Dist diff: ", driving_dist - actual_driven_dist

        if abs(driving_dist - actual_driven_dist) < 35:
            visitedLM[lastSeenLM] = True

        LMInSight = False

        #if driving_dist > 0:
        #    sleep(driving_dist/translationInOneSecond)
        #arlo.stop()
        
        # Move particles
       # for particle in particles: 
       #     dx=delt(paXarticle.getTheta(),actual_driven_dist)
       #     dy=deltaY(particle.getTheta(),actual_driven_dist)
       #     par.move_particle(particle, dx, -dy, lastMeasuredAngle)
        for particle in particles:
            dx = np.cos(particle.getTheta())*actual_driven_dist
            dy = np.sin(particle.getTheta())*actual_driven_dist
            par.move_particle(particle, dx, -dy, 0)
 
    elif not LMInSight or (LMInSight and visitedLM[lastSeenLM]) and not (visitedLM[0] and visitedLM[1]):

        if turn_counter < 8:
            turn_counter += 1
            print 'Turning around. Number of turns:', turn_counter

            # rotate 
            arlo.go_diff(30, 29, 0, 1)
            sleep((math.pi * 0.25) / rotationInOneSecond)
            arlo.stop()
            for particle in particles:
                par.move_particle(particle, 0, 0, -(math.pi * 0.25) / rotationInOneSecond)
                
                
        elif visitedLM[0] or visitedLM[1]: # Going around a box. Explore
        
            print 'Trying to go around a box in front of me'
            arlo.go_diff(80, 79, 0, 0)
            sleep(0.25)
            
            arlo.go_diff(30, 29, 1, 0)
            sleep((math.pi * 0.30) / rotationInOneSecond)
            
            
            driving_dist=30
            t = driving_dist/translationInOneSecond
            dt = 0.1
            current_time = 0
            stop_dist = 200
            while current_time < t:
                current_time += dt
    
                sensor_reads = [arlo.read_sensor(0), arlo.read_sensor(2), arlo.read_sensor(3)]
                print "Front: {0} - Left: {1} - Right: {2}".format(sensor_reads[0], sensor_reads[1], sensor_reads[2])
                if sensor_reads[0] < stop_dist or sensor_reads[1] < stop_dist or sensor_reads[2] < stop_dist: 
                    arlo.stop()
                    LMInSight = False
                    print "Sensor stopp!"
                    break
                arlo.go_diff(80, 79, 1, 1)
            arlo.stop()
        
        
            arlo.go_diff(30, 29, 0, 1)
            sleep((math.pi * 0.45) / rotationInOneSecond)
            arlo.stop()
            
            
            driving_dist=70
            t = driving_dist/translationInOneSecond
            dt = t / 100.0 + 0.05
            current_time = 0
            stop_dist = 200
            while current_time < t:
                current_time += dt
    
                sensor_reads = [arlo.read_sensor(0), arlo.read_sensor(2), arlo.read_sensor(3)]
                print "Front: {0} - Left: {1} - Right: {2}".format(sensor_reads[0], sensor_reads[1], sensor_reads[2])
                if sensor_reads[0] < stop_dist or sensor_reads[1] < stop_dist or sensor_reads[2] < stop_dist: 
                    arlo.stop()
                    LMInSight = False
                    print "Sensor stopp!"
                    break
                arlo.go_diff(80, 79, 1, 1)
                sleep(dt)
            arlo.stop()
            
            
            for particle in particles:
                dx = np.cos(particle.getTheta())*translationInOneSecond
                dy = np.sin(particle.getTheta())*translationInOneSecond
                par.move_particle(particle, dx, dy, -(math.pi * 0.50) / rotationInOneSecond)
            turn_counter = 0
    print "\n"
    # Draw map
    draw_world(est_pose, particles, world)
    
    # Show frame
    cv2.imshow(WIN_RF1, colour);

    # Show world
    cv2.imshow(WIN_World, world);
    
    
# Close all windows
cv2.destroyAllWindows()
