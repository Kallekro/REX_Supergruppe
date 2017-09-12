import time
from time import sleep
import sys

try:
  import robot
except:
  e = sys.exc_info()[0]
  print "Robot module not loaded"
  print "Error: %s" % e
  sys.exit()

def main(*arg):
  if len(arg) != 3:
    print "usage: turntime (seconds), direction (0 or 1)"      
  turn_time = int(arg[1])
  if turn_time <= 0:
    turn_time = 1      
  arlo = robot.Robot()
  if int(arg[2]) == 0:
    robot.left()
  else:
    robot.right()
  sleep(turn_time)
  arlo.stop()

if __name__ == "__main__":
  main(sys.argv)      

