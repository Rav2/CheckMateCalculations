#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import pylab
from matplotlib.colors import ListedColormap

if len(sys.argv) !=2:
	exit(1)
else:
	m1 = []
	m2 = []
	result = []
	with open(sys.argv[1], 'r') as file:
		for line in file:
			if line[0] == '#':
				pass
			else:
				splitted = line.split()
				m1.append(splitted[1])
				m2.append(splitted[2])
				result.append(splitted[3])
fig = plt.figure(figsize=(14,8))
colors= ['red' if l=='0' else 'green' for l in result]
plt.scatter(m1, m2, c=colors, marker='s', s=38, linewidth=0)
plt.xlabel("squark mass")
plt.ylabel("neutralino mass")
plt.title("QqN1")
plt.show()