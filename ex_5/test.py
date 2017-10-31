import cv2
import particle
import camera
import numpy as np



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
    p = particle.Particle(2000.0*np.random.ranf() - 1000, 2000.0*np.random.ranf() - 1000, 2.0*np.pi*np.random.ranf() - np.pi, 1.0/num_particles)
    #p = particle.Particle(2000.0*np.random.ranf() - 1000, 2000.0*np.random.ranf() - 1000, np.pi+3.0*np.pi/4.0, 1.0/num_particles)
    particles.append(p)

est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

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
        # XXX: You do this
"""
    for particle in particles:
        posWeight = 0;
        angleWeight = 0;
        if(objectType == 'horizontal'):
            calculated_distance = (math.sqrt(2**particle.getX + 2**particle.getY))
            if(calculated_distancePos < measured_distance):
                PosWeight = measured_distance/calculated_distance
                angleWeight = measured_angle/particle.getTheta()
            else:
                posWeight = calculated_distance/measured_distance
                angleWeight = particle.getTheta()/measured_angle
        elif(objectType == 'vertical'):
            calculated_distance = (math.sqrt(2**(particle.getX-300) + 2**particle.getY))
            if(calculated_distance < measured_distance):
                posWeight = measured_distance/calculated_distance
                angleWeight = measured_angle/particle.getTheta()
            else:
                posWeight = calculated_distance/measured_distance
                angleWeight = particle.getTheta()/measured_angle
            particle.setWeight() = posWeight*angleWeight


"""



    for particle in particles:
        posWeight = 0
        angleWeight = 0
        if(objectType == 'horizontal'):
            calculated_distance = (math.sqrt(2**particle.getX() + 2**particle.getY()))
            PosWeight = (1/math.sqrt(2*math.pi*sigma_d**2))*math.exp((-measured_distance-calculated_distance)/(2*sigma_distance**2)))
            angleWeight = (1/math.sqrt(2*math.pi*sigma_d**2))*math.exp((-measured_angle-particle.getTheta()/(2*sigma_theta**2)))
            elif(objectType == 'vertical'):
            calculated_distance = (math.sqrt(2**(particle.getX-300) + 2**particle.getY))
            PosWeight = (1/math.sqrt(2*math.pi*sigma_d**2))*math.exp((-measured_distance-calculated_distance)/(2*sigma_distance**2)))
            angleWeight = (1/math.sqrt(2*math.pi*sigma_d**2))*math.exp((-measured_angle-particle.getTheta()/(2*sigma_theta**2)))

        # Resampling
        # XXX: You do this

        # Draw detected pattern
        cam.draw_object(colour)
    else:
        # No observation - reset weights to uniform distribution
        for p in particles:
            p.setWeight(1.0/num_particles)

    
    est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

    # Draw map
    draw_world(est_pose, particles, world)
    
    # Show frame
    cv2.imshow(WIN_RF1, colour);

    # Show world
    cv2.imshow(WIN_World, world);
    
    
# Close all windows
cv2.destroyAllWindows()