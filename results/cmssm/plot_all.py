#!/usr/bin/env python
#
# This script draws 3D plots for the 4D grid. One plot per N1 mass value.
#
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt 
import matplotlib.colors as cls
import numpy as np
import pandas as pd

##################################################################

def do_plot(data, labels, zeroA0):
	# print(data)
	fig = plt.figure()
	ax = fig.add_subplot(111) 

	# plot size
	fig.subplots_adjust(bottom=0.15, right=0.97, top=0.90, left=0.18)

	# axes labels
	ax.set_xlabel('{}{}'.format(labels[0], r'$[GeV/c^2]$'), fontsize=16)
	ax.set_ylabel(labels[1]+r'$[GeV/c^2]$', fontsize=16)

	# extract data to plot
	xar = data['m0'].tolist()
	yar = data['mhalf'].tolist()
	zar = data['r'].tolist()

	# extract projection type
	tanval = str(data['tanB'].values[0])
	sign = str(data['sign'].values[0])
	if zeroA0:
		A0 = '0'
	else:
		A0 = '-mhalf'

	# axes ranges
	ax.set_xlim(0, 3100)
	ax.set_ylim(350, 1250)

	# ticks font
	plt.xticks(fontsize = 14) 
	plt.yticks(fontsize = 14) 

	# scatter plot
	vmin, vmax = 10**-2, 10
	sc = ax.scatter(xar, yar, s=130, c=zar, cmap='nipy_spectral', norm=cls.LogNorm(), 
		vmin=vmin, vmax=vmax, lw=0.5, edgecolors='none', marker='s', alpha=0.7, rasterized=False)  

	plt.title('r value for {}={}, {}={}, {}={}'.format(labels[2], tanval, labels[3], A0, labels[4], sign), fontsize = 18)
		  
	# color bar
	cb = plt.colorbar(sc)

	# chi2 = 0.05 contour
	lw_0 = 2.5
	lw_er = 1.5

	# levels = [0.05]
	new_zar = []
	for z in zar:
		if z >= 1.0:
			new_zar.append(1)
		else:
			new_zar.append(0)
	c_check = 'crimson'
	ax.tricontour(xar, yar, new_zar, 1, linewidths=lw_0, colors=c_check, linestyles='-')

	plt.savefig('plots/{}_{}_{}.png'.format(tanval, A0, sign))
	plt.close()
	plt.clf()


##################################################################

plot_prefix = 'cmssm'
infile = 'collective_results.txt'

labels = (r'$m_0$', r'$m_{1/2}$', r'$tan \beta$', r'$A_0$', r'$sgn(\mu)$')
# load data
data_raw = np.loadtxt(infile, skiprows=2, usecols=range(0,6))
data = data_raw.transpose()
assert len(labels)+1 == len(data), "Labels not set!" 

# plot m0 vs mhalf
df=pd.DataFrame(data_raw).sort_values(0)
df.columns = ['m0', 'mhalf', 'tanB', 'A0', 'sign', 'r']
gb = df.groupby(['tanB', 'sign'], sort=True)
groups = [gb.get_group(x) for x in gb.groups]
# Iterate over four groups (2 vals of tanBeta and signMu)
for gr in groups:
	gr = gr.apply(pd.to_numeric)
	# Two cases for A0, it's either 0 or -mhalf
	zeroA0 = gr[gr['A0'] == 0]
	nonzeroA0 = gr[gr['A0'] != 0]
	if not zeroA0.empty:
		do_plot(zeroA0, labels, True)
	if not nonzeroA0.empty:
		do_plot(nonzeroA0, labels, False)

