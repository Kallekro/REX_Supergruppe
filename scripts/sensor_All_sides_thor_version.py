
import time
from time import sleep
import robot

arlo = robot.Robot()


Right_speed=78
Left_speed=80
min_dist=400
def goStraight():
   print arlo.go_diff(Left_speed,Right_speed,1,1)


def goRight():
   print arlo.go_diff(Left_speed,Right_speed,1,0)

def goLeft():
    print arlo.go_diff(Left_speed,Right_speed,0,1)
    
tt=0.1


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
            if arlo.read_sensor(3)>arlo.read_sensor(2):
                print 'However, more space at right side than left'
                while arlo.read_sensor(0) < min_dist:
                    print 'Right HHH'
                    goRight()
                    
            elif arlo.read_sensor(3)<arlo.read_sensor(2):
                print 'However, more space at left side than right'
                while arlo.read_sensor(0) < min_dist:
                    print 'Left HHH'
                    goLeft()

        elif arlo.read_sensor(3)<min_dist and arlo.read_sensor(2)<min_dist:
                print 'SMALL space at both sides'
                if arlo.read_sensor(3)>arlo.read_sensor(2):
                    print 'However, more space at right side than left'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Right TTT'
                        goRight()
                        
                elif arlo.read_sensor(3)<arlo.read_sensor(2):
                    print 'However, more space at left side than right'
                    while arlo.read_sensor(0) < min_dist:
                        print 'Left TTT'
                        goLeft()


except KeyboardInterrupt:
    arlo.stop()
    print 'KEYBORARD INTERRUPT'
    pass
