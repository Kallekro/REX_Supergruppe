import time
import random
from time import sleep
import robot
import robot_constants as rc
arlo = robot.Robot()
import random 

frontPing = 2000; 
#leftPing = 2000;
#rightPing = 2000;
#backPing = 2000;
Right_speed=39
Left_speed=40

min_dist=40
def goStraight():
	arlo.go_diff(Left_speed,Right_speed,1,1)
def goRight():
	arlo.go_diff(Left_speed,Right_speed,1,0)
def goLeft():
	arlo.go_diff(Left_speed,Right_speed,0,1)

try:
    while 1:
        #print 'right ',arlo.read_sensor(3)
        #sleep(1)
        print 'left ',arlo.read_sensor(2)
        sleep(1)
        #print 'front ',arlo.read_sensor(0)
        #sleep(1)
        
except KeyboardInterrupt:
    arlo.stop()
    print 'KEYBORARD INTERRUPT'
    pass
        


