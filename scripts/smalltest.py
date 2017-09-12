import robot
import time
from time import sleep

arlo = robot.Robot()

#arlo.step_forward()
arlo.go()
sleep(7)
arlo.stop()
