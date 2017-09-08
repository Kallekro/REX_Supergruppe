import time
from time import sleep

import robot

arlo = robot.Robot()

left_speed = 180
right_speed = 60
elapsedSecs = 0
while elapsedSecs < 12:
 #arlo.step_rotate_lef t()
 arlo.go_diff(left_speed, right_speed, 1, 1)
 #arlo.left()
 sleep(6)
 arlo.go_diff(right_speed, left_speed, 1, 1)
 sleep(6)
 elapsedSecs += 12

print arlo.stop()

