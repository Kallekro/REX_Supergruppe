import time
from time import sleep

import robot

arlo = robot.Robot()

def drive_eight(n):
  """ Sends commands to Arlo to drive continuously in an eight-shaped route for n laps. Returns a string on completion."""
  # Variables for the go_diff function
  fast_speed = 80 
  slow_speed = 25
  # Half a lap time, this is the time the robot turns in a direction before switching
  half_lap_time =6.2 
  # To avoid having tu manually stop the robot we set it to drive continuously for x amount of seconds.
  elapsedSecs = 0
  while elapsedSecs < half_lap_time * 2 * n:
   arlo.go_diff(fast_speed, slow_speed, 1, 1)
   sleep(half_lap_time)
   arlo.go_diff(slow_speed, fast_speed, 1, 1)
   sleep(half_lap_time)
   elapsedSecs += half_lap_time * 2


print drive_eight(2) # Drive 10 eight-shaped laps 
print arlo.stop()


