#!/usr/bin/env python
import numpy as np
import os

# load grid data 
data_raw_grid = np.loadtxt('grid.dat', skiprows=1)
for row in data_raw_grid:
	for number in row:
		number = int(number)
# data_grid = data_raw_grid.transpose()

directory = '/RESULTS/grid4D/results'

dirs = [x[0].split('_') for x in os.walk(directory)]

ii = 0
for d in dirs:
	if d not in data_raw_grid:
		print(d)
		ii += 1
print(ii)