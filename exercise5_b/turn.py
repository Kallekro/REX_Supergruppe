import robot
import math
from time import sleep

arlo = robot.Robot()
count = 0

while count < 8:
    arlo.go_diff(30,29, 1,0)
    sleep(math.pi*0.25 / 0.78)
    arlo.stop()
    count += 1
    print count
    sleep(0.5)
