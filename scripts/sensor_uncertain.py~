import time
import random
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

import robot

arlo = robot.Robot()


sensor_to_meassure = 0
meassurements = np.arange(10)


for i in range(1):
    inp = raw_input()
    sensorread = arlo.read_sensor(sensor_to_meassure)
    meassurements[i] = sensorread
    
log_filename = "sensor{0}_log".format(sensor_to_meassure)
    
with open(log_filename, 'w') as f:
    for measure in meassurements:
        f.write(str(measure)+"\n")

    
        
    

        
