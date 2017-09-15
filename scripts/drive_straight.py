import time
from time import sleep
import sys

import robot



def main(arg):
  drive_time = int(sys.argv[1])
  if drive_time <= 0:
    drive_time = 1      
  arlo = robot.Robot()
  arlo.go_diff(25, 25, 1, 1)
  sleep(drive_time)
  arlo.stop()
  arlo.go_diff(25, 25, 0, 0)
  sleep(drive_time)
  arlo.stop()
  

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "usage: drive duration (seconds)"      
    sys.exit()
  main(sys.argv[1]) 

