import time
from time import sleep
import robot

import sys

def main(*arg):
  if len(arg) != 2:
    print "The program accepts exactly one argument"      
  drive_time = int(arg[1])
  if drive_time <= 0:
    drive_time = 1      
  arlo = robot.Robot()
  robot.go()
  sleep(drive_time)
  arlo.stop()
  

if __name__ == "__main__":
  main(sys.argv)      

