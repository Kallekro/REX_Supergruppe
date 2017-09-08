import time
from time import sleep
import robot

arlo = robot.Robot()

#for j in range(4):
for i in range(4):
  print arlo.go()
  sleep(5.8)
  print arlo.left()
  sleep(1.51)
  print arlo.stop()

#print arlo.go()
#sleep(5.5)
arlo.stop()
