import robot
from time import sleep

arlo = robot.Robot()

arlo.go_diff(40, 39, 1, 0)
sleep(1.38*4.0)
arlo.stop()
