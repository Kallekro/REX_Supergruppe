import time
from time import sleep

import robot

arlo = robot.Robot()

def drive_eight(n):
  """ Sends commands to Arlo to drive continuously in an eight-shaped route for n laps. Returns a string on completion."""
  # Variables for the go_diff function
  fast_speed = 127 
  slow_speed = 40
  # Half a lap time, this is the time the robot turns in a direction before switching
  half_lap_time = 6
  # To avoid having to manually stop the robot we set it to drive continuously for x amount of seconds.
  elapsedSecs = 0
  while elapsedSecs < half_lap_time * 2 * n:
   arlo.go_diff(fast_speed, slow_speed, 1, 1)
   sleep(half_lap_time)
   arlo.go_diff(slow_speed, fast_speed, 1, 1)
   sleep(half_lap_time)
   elapsedSecs += half_lap_time * 2
  return "Arlo ended 'eight' procedure"


print drive_eight(10) # Drive 10 eight-shaped laps 
print arlo.stop()


