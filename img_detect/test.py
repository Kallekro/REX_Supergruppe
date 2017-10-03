import time
from time import sleep
import robot
import picamera
import findObject
import cv2


Right_speed=39
Left_speed=40
min_dist=40
sleep_time=0.1
min_dist=30 #unit is centimeters

H=30 #height of the box in centimeters
scale=480
f=2533*scale/2464  #Average of theburning angel, scale is the height of the picture in pixels


arlo = robot.Robot()
def goStraight():
   print arlo.go_diff(Left_speed,Right_speed,1,1)
def goRight():
   print arlo.go_diff(Left_speed,Right_speed,1,0)
def goLeft():
    print arlo.go_diff(Left_speed,Right_speed,0,1)

    
Z = 99999
output_count=0        
    
def update_pic():
   global output_count
   with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)
      im_name = "img/org_img_{0}.jpg".format(output_count)      
      camera.capture(im_name)
   
      result, output_img = findObject.analyzeImage(im_name, 1.0, True) # the result class from the image analysis
        
      a=result.lenB # number of pixels left of the box
      b= result.lenA # number of pixels right of the box
      h=result.height # height og the box in pixels 
      isBox = result.isBox
      cv2.imwrite("img/Hueimg/hue_img_{0}.jpg".format(output_count), output_img)
      output_count += 1
      print "a=", a
      print "b=", b
      #print "isBox:", isBox      
      return a,b,h,isBox

a, b, h, isBox = update_pic()    

while Z>min_dist and isBox:    
    a,b,h,isBox = update_pic()
    print 'a=',a
    print 'b=',b
    
if not isBox:
    print 'Error there is no box in the picture'
