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
Data = np.loadtxt('data_lenght_vs_time.csv',skiprows=0,delimiter=';', dtype='float')
time = Data[:,0]
lenght = Data[:,1]
uncertainty_time=0.01
uncertainty_number_lenght = 20


plt.figure(1)
plt.figure(figsize=(13,10)) # er simplthen størrelsen på ruden af figuren
plt.errorbar(time, lenght, yerr=uncertainty_number_lenght, xerr=uncertainty_time, fmt='-', capsize=6, capthick=4, color='blue')
#plt.errorbar(timeS, lenghtS, xerr=uncertainty_time, fmt='.', capsize=3, capthick=2, color='black')

#(x[0:25],y[0:25],'.',ms=8.0, color='black') # prø a slette tallet 8.0 og farven er for de sorte prikker 
plt.xlabel('Time[s]', fontsize=20)
plt.ylabel('Lenght[cm]', fontsize=20)
plt.title('Lenght vs time', fontsize=30)
plt.legend()
savefig('Lenght vs time') # 
plt.show(block=False) #Thisblock=False is something that the program doesn't open up a new windows
# but just keep running the script. However I can't see the difference



