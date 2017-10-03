from __future__ import division
import numpy as np
import math


actual = np.load("actual.npy")
m1 = np.load("meth1.npy") 
m2 = np.load("meth2.npy") 
m3 = m1 * 1.122

def mean(arr):
    return sum(arr)/len(arr)

def abs_dists(arr1, arr2):
    ret =[]
    for i in range(len(arr1)):
        ret.append(abs(arr1[i] - arr2[i]))                   
    return ret, sum(ret)/len(ret)

def std(arr, mean):
    var = 0
    for el in arr:
        var += (el-mean)**2
    std = math.sqrt( (1/(len(arr)-1)) *var )
    return std

# For method 1 without scaling with focal length error ..
a, b = abs_dists(actual, m1) 
print "Std and mean for method 1: ", std(a,b), b

# For method 1 without scaling without focal length error ..
a, b = abs_dists(actual, m3)
print "Std and mean for method 1 (w focal length error): ", std(a,b), b

# Mehtod2
a, b = abs_dists(actual, m2)
print "Std and mean for method 2: ",std(a,b), b
