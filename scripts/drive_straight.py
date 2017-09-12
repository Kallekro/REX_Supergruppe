import time
from time import sleep
import robot

import sys

if __name__ == "__main__":
  drive_time = int(sys.argv[1])
  if drive_time <= 0:
    drive_time = 1      
  arlo = robot.Robot()
  arlo.go()
  sleep(drive_time)
  arlo.stop()

