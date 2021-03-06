from __future__ import division
import time
from time import sleep
import robot
import robot_constants

import robot_constants as rc

arlo = robot.Robot()
drive_a_meter_time = rc.one_meter_time / 4 
turn_90_degrees_time = rc.turn_90degrees_time 

def drive_square(straight_time, turn_time):
  """ Drive in a square, driving straight_time forward and turning for turn_time time (to achieve 90 degrees).
       We decided to supply these as arguments so that they can easily be tweaked. """
   # We just repeat the same instructions 4 times to drive in a square
 
  for i in range(4):
    arlo.go_diff( 79, 80, 1, 1)
    sleep(rc.one_meter_time)
    arlo.go_diff( 79, 80, 0, 1) 
    sleep(rc.turn_90degrees_time)

for i in range(10):
  drive_square(drive_a_meter_time, turn_90_degrees_time); # Drive in non-continuous square-shape   

arlo.stop()
