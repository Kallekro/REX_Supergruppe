
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
   sleep(.5)

def goRight():
   arlo.go_diff(Left_speed,Right_speed,1,0)
   sleep(.5)

def goLeft():
    arlo.go_diff(Left_speed,Right_speed,0,1)
    sleep(.5)

try:
    while 1:

        goStraight()

        if arlo.read_sensor(2) < min_dist:
                while arlo.read_sensor(2) < min_dist:
                    print 'Left side bloked'
                    print 'Right'
                    goRight()

        elif arlo.read_sensor(3) < min_dist:
                while arlo.read_sensor(3) < min_dist:
                    print 'Right side bloked'
                    print 'Left'
                    goLeft()

        elif arlo.read_sensor(0) < min_dist:
            if arlo.read_sensor(3)>min_dist and arlo.read_sensor(2)<min_dist:
                while arlo.read_sensor(0) < min_dist:
                    print 'Right YYY'
                    goRight()
            if arlo.read_sensor(3)<min_dist and arlo.read_sensor(2)>min_dist:
                while arlo.read_sensor(0) < min_dist:
                    print 'Left YYY'
                    goLeft()
            if arlo.read_sensor(3)>min_dist and arlo.read_sensor(2)>min_dist:
                print 'Space at both sides'
                if arlo.read_sensor(3)>arlo.read_sensor(2):
                    print 'However, more space at right side than left'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Right HHH'
                        goRight()
                if arlo.read_sensor(3)<arlo.read_sensor(2):
                    print 'However, more space at left side than right'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Left HHH'
                        goLeft()

                #IF ARLO has to chioce left or right side by random, use the following lines:
#            if arlo.read_sensor(3)>min_dist and arlo.read_sensor(2)>min_dist:
#                while arlo.read_sensor(0) < min_dist:
#                    print 'Either left or right'
#                    rnd=random.getrandbits(1)
#                    if rnd==0:
#                        while arlo.read_sensor(0) < min_dist:
#                            print 'Left'
#                            goLeft()
#                    if rnd==1:
#                        while arlo.read_sensor(0) < min_dist:
#                            print 'Right'
#                            goRight()
        elif arlo.read_sensor(3)<min_dist and arlo.read_sensor(2)<min_dist:
#                print 'STOP'
#                arlo.stop()
#                break
#               #If you want ARLo to take a random decision about turning right or left.
#                while arlo.read_sensor(0) < min_dist:
#                    print 'NARROW TRAP'
#                    rnd=random.getrandbits(1)
#                    if rnd==0:
#                        while arlo.read_sensor(0) < min_dist:
#                            print 'Left'
#                            goLeft()
#                    if rnd==1:
#                        while arlo.read_sensor(0) < min_dist:
#                            print 'Right'
#                            goRight()
                print 'SMALL space at both sides'
                if arlo.read_sensor(3)>arlo.read_sensor(2):
                    print 'However, more space at right side than left'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Right TTT'
                        goRight()
                if arlo.read_sensor(3)<arlo.read_sensor(2):
                    print 'However, more space at left side than right'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Left TTT'
                        goLeft()







except KeyboardInterrupt:
    arlo.stop()
    print 'KEYBORARD INTERRUPT'
    pass
