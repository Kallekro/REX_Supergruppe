import time
from time import sleep
import robot
import picamera
import findObject
import cv2


Right_speed=39
Left_speed=40
min_dist=80
sleep_time=0.1

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
      sleep(0.1)
      
      a=result.lenA # number of pixels left of the box
      b= result.lenB # number of pixels right of the box

      h=result.height # height og the box in pixels
      c_x=result.posX
      c_y=result.posY
      isBox = result.isBox
      cv2.imwrite("img/Hueimg/hue_img_{0}.jpg".format(output_count), output_img)
      output_count += 1
      print "a=", a
      print "b=", b
      print "posx:", c_x
      print "posy:", c_y
      #print "isBox:", isBox      
      return a,b,h,isBox

a, b, h, isBox = update_pic()    


while Z>min_dist and isBox:    
    tt = 0 #The only allows the robot to turn in one direction- If this wasn't defined the robot woudl just trun left and right all the rtime and not move forward
    if a>=b:
        while a>=b: 
            goRight()
            sleep(0.1)
            arlo.stop()
            a,b,h,isBox = update_pic()
            if not isBox:
               break
            tt = 1
                
    if a<=b and tt==0:
        while a<=b:
            goLeft()
            sleep(0.1)
            arlo.stop()       
            a,b,h,isBox = update_pic()
            if not isBox:
               break

    print isBox
    if not isBox:
       break
    
    Z=f*H/h       
    print "Distance:", Z        

    speed_scale=1 # THe robot is as standard set to 80-78 driving force. If this is downsize the speed_scale needs to be higer than 1 in order for the robot to drive half the lenght of Z
    drive_time=Z/50*speed_scale #The Arlo drives 50 centimers pr second, so therefore by diving Z with 50 yo get the drivetime
    goStraight()
    sleep(drive_time/2) #We devide the drive time with 2 in order to take multiple pictures along the way to the grren box


arlo.stop()

print "Reached distance = {0} from th box".format(Z)
#import os
#os.system('mpg321 song.mp3 &')
#
#print arlo.go_diff(125,125,0,1)


