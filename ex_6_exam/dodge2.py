import robot
import time
from time import sleep

arlo = robot.Robot()

Right_speed=78
Left_speed=80
min_dist=350

def sleep():
    sleep((math.pi * 0.25) / 0.73)

def updateSensor(sensor_id):
    return arlo.read_sensor(sensor_id)

def goStraight():
    arlo.go_diff(Left_speed,Right_speed,1,1)

def goRight():
    arlo.go_diff(Left_speed,Right_speed,1,0)

def goLeft():
    arlo.go_diff(Left_speed,Right_speed,0,1)
     

def dodgeBox():
    print "WHAT"
    dodged = False   
    sensor_reads = [arlo.read_sensor(0), arlo.read_sensor(2), arlo.read_sensor(3)]  # Front, Left, Right        
    
    if sensor_reads[1] > sensor_reads[2]:
        dir = "left"
    else:
        dir = "right"

    while not dodged:
        if dir == "left":
           while sensor_reads[2] < min_dist:
                goLeft()
                sleep()
                sensor_reads[2] = updateSensor(2)        
           arlo.stop()
           print "Right freee, GO!"
        
        elif dir == "right":
            while sensor_reads[1] < min_dist:
                goRight()
                sleep()
                sensor_reads[1] = updateSensor(1)
            arlo.stop()
            print "Left free, GO!"
    
    print "DONE."

dodgeBox()

