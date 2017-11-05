from __future__ import division
import robot
import math
import time
from time import sleep

arlo = robot.Robot()

rot_sec = 0.73

arlo.go_diff(30,29, 0,1)

sleep(0.7 / rot_sec)
arlo.stop()
