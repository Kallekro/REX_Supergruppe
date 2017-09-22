import time
import picamera
a=1

with picamera.PiCamera() as camera:
    camera.resolution = (3280,2464)
    print "Enter a name for the image."
    name = raw_input()
    camera.capture_sequence((
        'img%s.png' % name
        for i in range(0,a)
        ), use_video_port=True)
