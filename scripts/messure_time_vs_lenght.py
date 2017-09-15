import time
from time import sleep
import sys

import robot

drive_time=4
arlo = robot.Robot()
print arlo.go_diff(80, 78, 1, 1)
sleep(drive_time)
arlo.stop()
  





""""
import time
from time import sleep
import robot

time=1

arlo = robot.Robot()
arlo.go()
sleep(time)
arlo.stop()
"""
