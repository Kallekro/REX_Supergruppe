import robot
import time
from time import sleep
import math

arlo = robot.Robot()

Right_speed=38
Left_speed=40
min_dist=350

def rotate_sleep():
    sleep((math.pi * 0.25) / 0.73)

def update_sensors(sensor_list):
    sensor_list[0] =  arlo.read_sensor(0)
    sensor_list[1] = arlo.read_sensor(2)
    sensor_list[2] = arlo.read_sensor(3)

def goStraight():
    arlo.go_diff(80, 78,1,1)

def goRight():
    arlo.go_diff(Left_speed,Right_speed,1,0)

def goLeft():
    arlo.go_diff(Left_speed,Right_speed,0,1)
     

def dodgeBox():
    print "WHAT"
    dodged = False   
    
    while not dodged:
        sensor_reads = [arlo.read_sensor(0), arlo.read_sensor(2), arlo.read_sensor(3)]  # Front, Left, Right        
          
        update_sensors(sensor_reads)
        if sensor_reads[1] > sensor_reads[2]:
            dir = "left"            

        elif sensor_reads[1] < sensor_reads[2]:
            dir = "right"
  
        else:
          dir = "left"      

        print "DIRECTION", dir
        sleep(2)

        if dir == "left":  ## Go left about
            while sensor_reads[2] < min_dist or sensor_reads[0] < min_dist:
                goLeft()
                rotate_sleep()
                update_sensors(sensor_reads)  ## Update the sensors
                print "GO LEFT ABOUT"
            dodged = True

        else: ## Go right about
            while sensor_reads[1] < min_dist or sensor_reads[0] < min_dist:
                goLeft()
                rotate_sleep()   ## Rotate 45 degrees
                update_sensors(sensor_reads)  ## Update the sensors
            print "GO RIGHT ABOUT"
            dodged = True
dodgeBox()
