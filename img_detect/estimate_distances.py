from __future__ import division
import robot
import numpy as np
import picamera
import findObject
import cv2
from time import sleep

arlo = robot.Robot()

Right_speed=79
Left_speed=80

method1_dists=[]
method2_dists=[]
actual_dists=[]

def goStraight():
   print arlo.go_diff(Left_speed,Right_speed,1,1)

real_height=31.0 #height of the box in centimeters
scale=480
focal_len=2533*scale/2464  #Average of theburning angel, scale is the height of the picture in pixels

p1 = 0
p2 = 0
drive_dist = 40 # centimeters 

def get_distance_m1 (f, H, h):
  if h == 0:
     print "No box from method 1"
     return 0
  return f*H/h

def get_distance_m2 (p1, p2, dist_driven):
  if p1 == 0 or p2 == 0 or (p2-p1) == 0:
    return 0
  else:
    return dist_driven * p1/(p2-p1)

def getResult():
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    im_name = "img/temp_img.jpg"
    camera.capture(im_name)
  
    result, output_img = findObject.analyzeImage(im_name, 1.0, True) # the result class from the image analysis
    return result

def estimate_distance (f, H, D):
  real_dist = arlo.read_front_ping_sensor()/10
  res = getResult()
  meth1 = get_distance_m1(f, H, res.height)
  p1 = res.height
  goStraight()
  sleep(D/50)
  arlo.stop()
  res = getResult()
  p2 = res.height
  meth2 = get_distance_m2(p1, p2, D)

  print "Sensor meassured distance: %d" %real_dist
  print "Distance estimated with method 1: %d" %meth1
  print "Distance estimated with method 2: %d"%(meth2+D)

  return real_dist, meth1, meth2+D

for i in range(5):
   rd, m1, m2 = estimate_distance(focal_len, real_height, drive_dist)
   actual_dists.append(rd)
   method1_dists.append(m1)
   method2_dists.append(m2)
   raw_input("Press enter to take new measurement")

np.save("actual-"+saveArr, np.array(actual_dists))
np.save("meth1-"+saveArr, np.array(method1_dists))
np.save("meth2"+saveArr, np.array(method2_dists))

loaded = np.load("data")
print loaded

   
