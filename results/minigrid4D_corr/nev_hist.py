#!/usr/bin/python
#
# This script plots a histogram with the distribution of the number of events to simulate.
#
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
	print("./nev_hist.py [FILE]")
	exit(1)

file = sys.argv[1]
data_raw = np.loadtxt(file, skiprows=2)
data = data_raw.transpose()
fig, ax = plt.subplots()
ax.hist(data[-1], 100)
ax.set_xlabel('Number of events to simulate')
ax.set_ylabel('Occurence')
# ax.set_xlim(1*10**6)
plt.title('Histogram of nev')
# ax.ticklabel_format(axis='x', useOffset=False, scilimits=(3,8))

plt.show()
