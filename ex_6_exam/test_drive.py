from __future__ import division
import robot
import time
from time import sleep

translationInOneSecond = 200

def driveArlo(dt, t, speedLeft = 80, speedRight = 79): 
  actual_driven_dist, current_time, c = 0.0, 0.0, 0.0 
  global avoiding_box 
  while current_time < t: 
      a = time.clock() 
      current_time += dt 
      actual_driven_dist += dt * translationInOneSecond 
 
      arlo.go_diff(speedLeft, speedRight, 1, 1) 
      b = time.clock() 
      c = b - a 
      print dt, c, current_time
      sleep(dt) 
  arlo.stop()
  return actual_driven_dist 

arlo  = robot.Robot()
driveArlo(2/25,2.0)

