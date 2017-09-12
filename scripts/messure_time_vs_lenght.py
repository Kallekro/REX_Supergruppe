import time
from time import sleep
import robot

time=1

arlo = robot.Robot()
arlo.go()
sleep(time)
arlo.stop()