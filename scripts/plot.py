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
Data = np.loadtxt('data.csv')
distance = Data[:,0]
number_clusters = Data[:,1]

"""
uncertainty_number_cluster = sqrt(number_clusters)
uncertainty_distance=0.13


#alt nedenståennde er fordi du du ikke fitter på hele resultatet med kun for de første 18 datapunkter - alt resten skæres altså væk.
Nnumber_clustersS = 18  #Look at the datasheet to see which distance the number Nnumber_clustersS corresponds to.
# Defining the short distance for the values for fitting. S=short
distanceS = distance[0:Nnumber_clustersS]
number_clustersS = number_clusters[0:Nnumber_clustersS]
uncertainty_number_clusterS=uncertainty_number_cluster[0:Nnumber_clustersS]



#Den formel du fitter efter
def f_c0R2(distanceS,c0):
	return c0/distanceS**2

#Der fittes med curve_fit
init_pars1 = [100000.0] #Startværider - skabes ved at du pøver at plotte i maple, og ser hvad der nogenlunde ligner dataen
Alpha_fit1 = curve_fit(f_c0R2,distanceS,number_clustersS, p0=init_pars1, maxfev=100000) #Maxfev er noget med hvor lang tid den maximalt har til at finde de fittede værdier. Hvis denne er lav, kan det være at spyder ikke komme frem til et resultat
Cov1=Alpha_fit1[1] #Man kan få flere frskellige ting ud af curve_fit men jeg vælger 1. mulighed
Parameter1 = Alpha_fit1[0]  #I don't undertand why this is nessasary but it is.
Parametererror1=np.sqrt(Cov1) #Danner en matrice hvor elementerne i diagonalen er usikkehede på de fittede værdier. Vil være ret stor for pågælnde datasæt, da den brugte funktion er for simpel 

                       
#De forventede værdier udregnes:
expected1=[]
for i in range(0,Nnumber_clustersS):
    fit1=f_c0R2(distanceS[i],Parameter1[0])
    expected1.append(fit1)


print '-------------------------------------------------------------------'
print('parameters from fit')
print('c[0] = %f ' %(Parameter1[0]))
print 'Parametererror1=', Parametererror1
chi1=stats.chisquare(number_clustersS, expected1 ) 
print 'chi1=',chi1 # Chisquare værdien vil her være meget lille, da den brugte funktion er for simpel 

#Kaos fit - kan bruges ligesom dette chi^2fit
#ks1=stats.ks_2samp(number_clustersS, expected1 )
#print 'Kaos teori', ks1
print '-------------------------------------------------------------------'

# Python graph plotting
#----------------------------------------------------------------------------------- #
plt.figure(figsize=(13,10)) # er simplthen størrelsen på ruden af figuren
plt.errorbar(distanceS, number_clustersS, yerr=uncertainty_number_clusterS, fmt='.', capsize=3, capthick=2, color='black')
plt.errorbar(distanceS, number_clustersS, xerr=uncertainty_distance, fmt='.', capsize=3, capthick=2, color='black')
#(x[0:25],y[0:25],'.',ms=8.0, color='black') # prø a slette tallet 8.0 og farven er for de sorte prikker 
plt.plot(distanceS,f_c0R2(distanceS,Parameter1[0]),color='r',label='C0/R^2')
plt.xlabel('Distance from alpha-source')
plt.ylabel('Number of cluters / time unit')
plt.title('Fit of a graph')
plt.legend()
savefig('Afstand fit graf CHI.jpeg') # 
plt.show(block=False) #Thisblock=False is something that the program doesn't open up a new windows
# but just keep running the script. However I can't see the difference



#----------------------------------------------------------------------------------- #
"""
