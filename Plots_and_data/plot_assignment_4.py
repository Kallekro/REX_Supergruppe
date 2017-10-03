import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import poisson
from scipy import stats
from scipy.optimize import minimize
import warnings
from pylab import * #

warnings.filterwarnings("ignore")
SavePlots = False        


#----------------------------------------------------------------------------------- #
# Reading the data:
#----------------------------------------------------------------------------------- #
plt.close('all')

actual =sort( np.load('actual.npy'))
meth1 = sort(np.load('meth1.npy'))
meth2 = sort(np.load('meth2.npy'))
b= np.mean(actual/meth1)
meth1_time_a_factor=sort(np.load('meth1.npy'))*b





#Data = np.loadtxt('data_lenght_vs_time.csv',skiprows=0,delimiter=';', dtype='float')

tt=0.1

plt.figure(2)
plt.figure(figsize=(13,10)) # er simplthen størrelsen på ruden af figuren
plt.errorbar(actual, meth1, fmt='-', yerr=tt, xerr=tt,  capsize=6, capthick=4, color='blue', label='Focal lenght method f*H/h')
plt.errorbar(actual, meth2, fmt='-', yerr=tt, xerr=tt, capsize=6, capthick=4, color='red', label='Moving method  D/(p1-p2)')
plt.errorbar(actual, actual, fmt='-', yerr=tt, xerr=tt, capsize=6, capthick=4, color='green', label='Actual lenght - messured from senors')
plt.errorbar(actual, meth1_time_a_factor, fmt='-', yerr=tt, xerr=tt,  capsize=6, capthick=4, color='yellow', label='Focal lenght times 1.1229')


#plt.errorbar(timeS, lenghtS, xerr=uncertainty_time, fmt='.', capsize=3, capthick=2, color='black')

#(x[0:25],y[0:25],'.',ms=8.0, color='black') # prø a slette tallet 8.0 og farven er for de sorte prikker 
plt.xlabel('Sensor distance[cm]', fontsize=20)
plt.ylabel('Messure distance with camera[cm]', fontsize=20)
plt.legend()
plt.title('Distance mesure with sensor vs camera', fontsize=30)
#plt.legend()
plt.legend(loc=2, prop={'size': 18})
savefig('Distance mesure with sensor vs camera') # 
plt.show(block=False) #Thisblock=False is something that the program doesn't open up a new windows
# but just keep running the script. However I can't see the difference



