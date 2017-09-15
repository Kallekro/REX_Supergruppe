import matplotlib.pyplot as plt
import numpy as np

dists = [10, 25, 50, 100, 150, 300]

data = np.arange(10)

print "What sensor data to plot?"
sensor = int(raw_input())


for dist in dists:
    index = 0
    with open("sensor_data/sensor{0}_dist{1}_log".format(sensor,dist), 'r') as f:
        for line in f:
            data[index] = int(line)
            index += 1

            
    plt.hist(data)
    plt.show()
