import robot_constants as rc

frontPing = 200;
leftPing = 200;
rightPing = 200;

try:
    while True:
        #rc.updatePings(leftPing,rightPing,frontPing)
        frontPing = rc.arlo.read_sensor(0)
        leftPing = rc.arlo.read_sensor(2)
        rightPing = rc.arlo.read_sensor(3)

        print "This is front ping: ", frontPing
        print "This is min dist fron: ", rc.min_dist_front
        if(frontPing > rc.min_dist_front): #and leftPing > rc.min_dist_left and rightPing > rc.min_dist_right):
            #rc.goStraight()
            rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,1)
        else:
            rc.arlo.stop()

#
#try:
#    while True:
#        #rc.updatePings(leftPing,rightPing,frontPing)
#        frontPing = rc.arlo.read_sensor(0)
#        leftPing = rc.arlo.read_sensor(2)
#        rightPing = rc.arlo.read_sensor(3)
#
#        print "This is front ping: ", frontPing
#        print "This is min dist fron: ", rc.min_dist_front
#        if(frontPing > rc.min_dist_front): #and leftPing > rc.min_dist_left and rightPing > rc.min_dist_right):
#            #rc.goStraight()
#            rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,1)
#        elif(frontPing < rc.min_dist_front): #and leftPing > rc.min_dist_left and rightPing > rc.min_dist_right):
#
#            #leftOrright = (int) (random.uniform(0, 2))
#                #rc.turnLeft(leftPing,rightPing,frontPing)
#                while(frontPing < 50):
#                    frontPing = rc.arlo.read_sensor(0)
#                    leftPing = rc.arlo.read_sensor(2)
#                    rightPing = rc.arlo.read_sensor(3)
#                    rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,0,1)
#	            rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,1)
#
#        elif(frontPing < rc.min_dist_front and leftPing < rc.min_dist_left and rightPing > rc.min_dist_right):
#            #rc.turnRight(leftPing,rightPing,frontPing)
#                while(frontPing < 50):
#                    frontPing = rc.arlo.read_sensor(0)
#                    leftPing = rc.arlo.read_sensor(2)
#                    rightPing = rc.arlo.read_sensor(3)
#                    rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,0)
#	            rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,1)
#
#        elif(frontPing < rc.min_dist_front and leftPing > rc.min_dist_left and rightPing < rc.min_dist_right):
#            #rc.turnLeft(leftPing,rightPing,frontPing)
#            while(frontPing < 50):
#                frontPing = rc.arlo.read_sensor(0)
#                leftPing = rc.arlo.read_sensor(2)
#                rightPing = rc.arlo.read_sensor(3)
#                rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,0,1)
#            rc.arlo.go_diff(rc.max_speed_left,rc.max_speed_right,1,1)
#

except KeyboardInterrupt:
    print rc.arlo.stop()
    pass
