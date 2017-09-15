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

def main():
  if len(sys.argv) != 3:
    print "usage: turntime (seconds), direction (0 or 1)"      
  turn_time = float(sys.argv[1])
  if turn_time <= 0:
    turn_time = 1      
  arlo = robot.Robot()
  if int(sys.argv[2]) == 0:
    arlo.go_diff(50, 50, 1, 0)
  else:
    arlo.go_diff(50, 50, 0, 1)
  sleep(turn_time)
  arlo.stop()

if __name__ == "__main__":
  main()      

