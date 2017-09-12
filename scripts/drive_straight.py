import time
from time import sleep
import sys

import robot

arlo = robot.Robot()

def main(arg):
  drive_time = int(arg)
  if drive_time <= 0:
    drive_time = 1      
  arlo.go()
  sleep(drive_time)
  arlo.stop()
  

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "usage: drive duration (seconds)"      
    sys.exit()
  main(sys.argv[1]) 

