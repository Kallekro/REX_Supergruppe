import time
from time import sleep
import robot

import sys

if __name__ == "__main__":
  turn_time = int(sys.argv[1])
  if turn_time <= 0:
    turn_time = 1      
  arlo = robot.Robot()
  robot.go()
  sleep(turn_time)
  arlo.stop()

