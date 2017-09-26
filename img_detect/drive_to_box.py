import time
from time import sleep
import robot
import picamera
import findObject

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

    
    
def update_pic():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.capture('Current_picture.jpg')

        result = findObject.analyzeImage('Current_picture.jpg', 1.0) # the result class from the image analysis
    
        a=result.lenA # number of pixels left of the box
        b= result.lenB# number of pixels right of the box
        h=result.height # height og the box in pixels 
        isBox = result.isBox
        return a,b,h,isBox

Z = 99999

a, b, h, isBox = update_pic()    

print isBox

while Z>min_dist and isBox:
    correct = True #The only allows the robot to turn in one direction- If this wasn't defined the robot woudl just trun left and right all the rtime and not move forward
    if a>=b:
        while a>=b: 
            goRight()
            sleep(0.1)
            arlo.stop()
            a,b,h,isBox = update_pic() 
            correct = False
        
    if a<=b and correct:
        while a<=b:
            goLeft()
            sleep(0.1)
            arlo.stop()       
            a,b,h,isBox = update_pic()
        
    if not isBox:
        break
    
    Z=f*H/h       
    print Z
    speed_scale=2 # THe robot is as standard set to 80-78 driving force. If this is downsize the speed_scale needs to be higer than 1 in order for the robot to drive half the lenght of Z
    drive_time=Z/50*speed_scale #The Arlo drives 50 centimers pr second, so therefore by diving Z with 50 yo get the drivetime
    goStraight()
    sleep(drive_time/2) #We devide the drive time with 2 in order to take multiple pictures along the way to the grren box
        
if not isBox:
    print 'Error there is no box in the picture'
