import cv2
import particle as par
import camera
import numpy as np
import math
import random_numbers as rnd
import copy

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

sigma_distance= 25.0 # chose a number
sigma_theta=2.0

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in cm.
landmarks = [(0.0, 0.0), (300.0, 0.0)]


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
num_particles = 1000
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

# Allocate space for world map
world = np.zeros((500,500,3), dtype=np.uint8)

# Draw map
draw_world(est_pose, particles, world)

print "Opening and initializing camera"

#cam = camera.Camera(0, 'macbookpro')
#cam = camera.Camera(0, 'frindo')
cam = camera.Camera(0, 'arlo')

while True:
    # Move the robot according to user input (for testing)
    action = cv2.waitKey(10)
    
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

    # XXX: Make the robot drive
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
         
        weight_sum = 0
        for particle in particles:
           posWeight = 0;
           angleWeight = 0;
           if objectType == 'horizontal':
               lm = landmarks[0]
           else:
               lm = landmarks[1]

           calculated_distance = (math.sqrt((particle.getX()-lm[0])**2 + ((particle.getY()-lm[1]))**2))

           if(calculated_distance < measured_distance):
               lol = rnd.randn(calculated_distance, sigma_distance)
               #if calculated_distance < 100:
               #    print "dist: ", calculated_distance
               #    print "LOL: ", lol
               #posWeight = abs(measured_distance - lol)
               #posWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_distance-calculated_distance)**2/(2*sigma_distance**2))
               posWeight = measured_distance/calculated_distance
               angleWeight = measured_angle/particle.getTheta() 
           else:
               lol = rnd.randn(calculated_distance, sigma_distance)
               #posWeight = abs(measured_distance - lol)
               #posWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_distance-calculated_distance)**2/(2*sigma_distance**2))
               #posWeight = measured_distance - rnd.randn(calculated_distance, sigma_distance**2)
               posWeight = calculated_distance/measured_distance
               angleWeight = particle.getTheta()/measured_angle

           particle.setWeight(posWeight)
           if particle.getWeight() < 0 or calculated_distance < 0:
               print "WHAT", particle.getWeight(), calculated_distance
           weight_sum += posWeight 

        #weight_sum = 0
        #for particle in particles:
        #    PosWeight = 0
        #    angleWeight = 0
        #    if(objectType == 'horizontal'):
        #        calculated_distance = math.sqrt(particle.getX()**2 + particle.getY()**2)
        #        PosWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_distance-calculated_distance)**2/(2*sigma_distance**2))
        #        angleWeight = (1/math.sqrt(2*math.pi*sigma_distance**2  ))*math.exp(-1*(measured_angle-particle.getTheta())**2/(2*sigma_theta**2))
        #    elif(objectType == 'vertical'):
        #        calculated_distance = (math.sqrt((particle.getX()-300)**2 + particle.getY()**2))
        #        PosWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_distance-calculated_distance)**2/(2*sigma_distance**2))
        #        angleWeight = (1/math.sqrt(2*math.pi*sigma_distance**2))*math.exp(-1*(measured_angle-particle.getTheta())**2/(2*sigma_theta**2))
        #    newWeight = PosWeight*angleWeight     
        #    if newWeight < 0.01:
        #       newWeight = 0.01 
        #    particle.setWeight(newWeight)

        #    weight_sum += newWeight 

        normsum = 0
        for particle in particles:
           particle.setWeight(particle.getWeight()/weight_sum) 
           normsum += particle.getWeight() 
           if particle.getWeight() > 0.1:
               print "Particle: ", particle.getWeight()

        # Resampling
        # XXX: You do this
        # weights = []
        # for i in 100:
        #     weights.append(rn.randn(0.0, 1.0))

        weights = [] 

        #print "sum {0}".format(weight_sum)

        cumsum = [0.0]
        tsum = 0
        for i in particles:
            w = i.getWeight()
            tsum += w
            cumsum.append(tsum)

        print "Sum of weights: ", cumsum[-1], " or ", normsum
        
        #resample_n = 1000
        for i in range(len(particles)):
           sample = np.random.ranf()
           for j in range(1, len(particles)):
               if sample >= cumsum[j-1] and sample < cumsum[j]:
                   particles[i] = copy.deepcopy(particles[j])
        
        # Draw detected pattern
        cam.draw_object(colour)

    else:
        # No observation - reset weights to uniform distribution
        for p in particles:
            p.setWeight(1.0/num_particles)

    #par.add_uncertainty(particles, 1.0, 0.05)

    
    est_pose = par.estimate_pose(particles) # The estimate of the robots current pose

    # Draw map
    draw_world(est_pose, particles, world)
    
    # Show frame
    cv2.imshow(WIN_RF1, colour);

    # Show world
    cv2.imshow(WIN_World, world);
    
    
# Close all windows
cv2.destroyAllWindows()
