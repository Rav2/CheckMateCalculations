#!/usr/bin/env python

import numpy as np 
import matplotlib.pyplot as plt 

infile = 'collective_results.txt'
data_raw = np.loadtxt(infile, skiprows=2, usecols=range(0,5))
data = data_raw.transpose()
n1 = data[3]
# print(n1)
plt.hist(n1, 10)
plt.show()
