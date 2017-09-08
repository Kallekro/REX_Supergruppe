import time
from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# Set speed
print arlo.set_speed(64)
print arlo.set_turnspeed(72)
print arlo.set_step_time(2000)
print arlo.set_turn_time(1500)

sleep(1)

# Reset the wheel encoders
arlo.reset_encoder_counts()

# send a go command
print arlo.go()

# Wait a bit while robot moves forward
sleep(3)

# send a stop command
print arlo.stop()

# request to read Front sonar ping sensor
print "Front sensor = ", arlo.read_front_ping_sensor()

# request to read Back sonar ping sensor
print "Back sensor = ", arlo.read_back_ping_sensor()

# request to read Right sonar ping sensor
print "Right sensor = ", arlo.read_right_ping_sensor()

# request to read Left sonar ping sensor
print "Left sensor = ", arlo.read_left_ping_sensor()


# send a go_diff command to drive forward in a curve turning right
leftSpeed = 128
rightSpeed = 100
print arlo.go_diff(leftSpeed, rightSpeed, 1, 1)

# Wait a bit while robot moves forward
sleep(3)

# send a stop command
print arlo.stop()


# send a go_diff command to drive backwards the same way we came from
print arlo.go_diff(leftSpeed, rightSpeed, 0, 0)

# Wait a bit while robot moves backwards
sleep(3)

# send a stop command
print arlo.stop()

# read the wheel encoders
print "Left wheel encoder = ", arlo.read_left_wheel_encoder()
print "Right wheel encoder = ", arlo.read_right_wheel_encoder()
        

print("Finished")
