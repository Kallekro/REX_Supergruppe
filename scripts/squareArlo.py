import time
from time import sleep
import robot

import robot_constants as rc

arlo = robot.Robot()
drive_a_meter_time = 5.8
turn_90_degrees_time = 1.35 

def drive_square(straight_time, turn_time):
  """ Drive in a square, driving straight_time forward and turning for turn_time time (to achieve 90 degrees).
       We decided to supply these as arguments so that they can easily be tweaked. """
   # We just repeat the same instructions 4 times to drive in a square
 
  for i in range(4):
    #print arlo.go()
    arlo.go_diff(50, 50, 1, 1)
    sleep(rc.one_meter_time)
    arlo.stop()
    arlo.go_diff(50, 50, 0, 1) 
    sleep(rc.turn_90degrees_time)
    print arlo.stop()

drive_square(drive_a_meter_time, turn_90_degrees_time); # Drive in non-continuous square-shape   

#for i in range(4):w

#  print arlo.go()
#  sleep(drive_a_meter_time )
#  print arlo.left()
#  sleep(turn_90_degrees_time)

arlo.stop()
