import time
import random
from time import sleep

import robot

arlo = robot.Robot()



frontPing = 2000;
leftPing = 2000;
rightPing = 2000;
backPing = 2000;

while(1):
    frontPing = arlo.read_sensor(0)
    leftPing = arlo.read_sensor(2)
    rightPing = arlo.read_sensor(3)
    backPing = arlo.read_sensor(1)

    if(frontPing > 50 && leftPing > 50 && rightPing > 50):
        arlo.go_diff(80,80,1,1)
    else if(frontPing < 50 && leftPing < 50 && rightPing < 50 && backPing > 50):
        arlo.go_diff(80,80,0,0)
    else if(frontPing < 50 && leftPing > 50 && rightPing > 50):
        leftOrright = random.rand(0,1)
        if( leftOrright == 0 ):
            #turn left
            #moveforward
        else:
            #turn right
            #moveforward
arlo.stop()
