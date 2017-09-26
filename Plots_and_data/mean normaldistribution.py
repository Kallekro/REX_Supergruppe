import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


#take title of plot
#Tage axe title arguments
#take point, if wanted, to plot on normal distribution
#take range of x value, and the density

x = [17,22,17,17.5,19,22,17.5]
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax2 = fig.add_subplot(1,1,1)
ax2.scatter(x,[.01,.02,.03,.04,.05,.06,.07],color='red')

x_axis = np.arange(10,25,0.01)
plt.plot(x_axis,norm.pdf(x_axis,18.5,2.25))


fig.suptitle('The normal distribution, of the square run.\n mean = 18.8 cm, and standard dev = 2.25\n from a sampel of 7 data')
ax.set_xlabel('Distance from starting point in cm after one run-through\n The red points are our measured data. The y only symbolis the order in which they were measured')
plt.show()
