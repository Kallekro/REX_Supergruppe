
import time
from time import sleep
import robot

arlo = robot.Robot()
sleep(2)

frontPing = 200
leftPing = 200
rightPing = 200
Right_speed=39
Left_speed=40
min_dist=40

def goStraight():
    print "Go straight: ", arlo.go_diff(Left_speed,Right_speed,1,1)
    sleep(1)
def goRight():
    print "Go right: ", arlo.go_diff(Left_speed,Right_speed,1,0)
    sleep(1)
def goLeft():
    print "Go left: ", arlo.go_diff(Left_speed,Right_speed,0,1)
    sleep(1)

def updateSensor(sensorID):
    sensor = arlo.read_sensor(sensorID)
    return sensor

try:
    while 1:
        #print arlo.stop()
        frontPing = updateSensor(0)
        print frontPing
        leftPing = updateSensor(2)
        print leftPing
        rightPing = updateSensor(3)
        print rightPing
        sleep(0.2)
        goStraight()


        if leftPing < min_dist:
                while leftPing < min_dist:
                    print 'Left side bloked'
                    print 'Right'
                    goRight()
                    leftPing = updateSensor(2)

        elif rightPing < min_dist:
                while rightPing < min_dist:
                    print 'Right side bloked'
                    print 'Left'
                    goLeft()
                    rightPing = updateSensor(3)

        elif frontPing < min_dist:
            if rightPing>min_dist and leftPing<min_dist:
                while frontPing < min_dist:
                    print 'Right YYY'
                    goRight()
                    frontPing = updateSensor(0)
            elif rightPing<min_dist and leftPing>min_dist:
                while frontPing < min_dist:
                    print 'Left YYY'
                    goLeft()
                    frontPing = updateSensor(0)
            elif rightPing>min_dist and leftPing>min_dist:
                print 'Space at both sides'
                if rightPing>leftPing:
                    print 'However, more space at right side than left'
                    while frontPing < min_dist:
                        print 'Right HHH'
                        goRight()
                        frontPing = updateSensor(0)
                elif rightPing<leftPing:
                    print 'However, more space at left side than right'
                    while frontPing < min_dist:
                        print 'Left HHH'
                        goLeft()
                        frontPing = updateSensor(0)

        elif rightPing<min_dist and leftPing<min_dist:
                print 'SMALL space at both sides'
                if rightPing>leftPing:
                    print 'However, more space at right side than left'
                    while frontPing < min_dist:
                        print 'Right TTT'
                        goRight()
                        frontPing = updateSensor(0)
                elif rightPing<leftPing:
                    print 'However, more space at left side than right'
                    while frontPing < min_dist:
                        print 'Left TTT'
                        goLeft()
                        frontPing = updateSensor(0)


except KeyboardInterrupt:
    arlo.stop()
    print 'KEYBORARD INTERRUPT'
    pass
