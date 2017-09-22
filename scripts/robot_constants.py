# Script for defining robot constants
# Start by importing this 
import time
import random
from time import sleep
import robot

arlo = robot.Robot()

one_meter_time = 2 
turn_90degrees_time = 1 
max_speed_left = 80
max_speed_right = 78
min_dist_front = 100
min_dist_left = 50
min_dist_right = 50
min_dist_back = 50

def goStraight():
	arlo.go_diff(max_speed_left,max_speed_right,1,1)

def updatePings(lPing,rPing,fPing): #bPing):
	fPing = arlo.read_sensor(0)	
        lPing = arlo.read_sensor(2)
        rPing = arlo.read_sensor(3)

def turnLeft(lPing,rPing,fPing):
	while(fPing < 50):
		updatePing(lPing,rPing,fPing)
		arlo.go_diff(max_speed_left,max_speed_right,0,1)
	goStraight()

def turnRight(lPing,rPing,fPing):
	while(fPing < 50):
		updatePing(lPing,rPing,fPing)
		arlo.go_diff(max_speed_left,max_speed_right,1,0)
	goStraight()

