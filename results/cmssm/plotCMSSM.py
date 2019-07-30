#!/usr/bin/env python

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt 
import matplotlib.colors as cls
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
##################################################################

def do_plot(data, labels, zeroA0, cmap='nipy_spectral', save=True):
	# print(data)
	fig = plt.figure(figsize=(6.4, 5.0))
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
	zar = [val if val>0 else 10**-15 for val in zar]

	# extract projection type
	tanval = str(int(data['tanB'].values[0]))
	sign = str(int(data['sign'].values[0]))
	if zeroA0:
		A0 = '0'
		A0_text = '0'
	else:
		A0 = r'-$m_{1/2}$'
		A0_text = '-mhalf'
	# print info
	z_quant = [0 if value < 1 else 1 for value in zar]
	print('--- INFO ABOUT cMSSM SCAN ---')
	print('tanB={}, A0={}, sgn={}'.format(tanval, A0_text, sign))
	print('allowed={}, excluded={}, total={}, excl. fraction={}'.format(len(z_quant)-sum(z_quant), sum(z_quant), len(z_quant), \
	                                                                    float(sum(z_quant))/float(len(z_quant))))

	# axes ranges
	ax.set_xlim(0, 3100)
	ax.set_ylim(350, 1250)

	# ticks font
	plt.xticks(fontsize = 14) 
	plt.yticks(fontsize = 14) 

	# scatter plot
	vmin, vmax = 0.55*10**-1, 10**2
	# Recreate UML color map
	colors1 = plt.cm.hot(np.linspace(0.5, 0.1, 128))
	colors2 = plt.cm.summer(np.linspace(0.0, 0.5, 128))
	colors = np.vstack((colors2, colors1))
	mymap = cls.LinearSegmentedColormap.from_list('my_colormap', colors)
	# nipy_spectral
	colormap = cmap
	if colormap == 'mymap':
		colormap = mymap
	if colormap != None:
		sc = ax.scatter(xar, yar, s=130, c=zar, cmap=colormap, norm=cls.LogNorm(), \
			vmin=vmin, vmax=vmax, lw=0.5, edgecolors='none', marker='s', alpha=0.7, rasterized=False) 
		# color bar
		cb = plt.colorbar(sc, shrink=0.9) 
		cb.ax.set_title('r', fontsize=10)
	plt.title('r value for {}={}, {}={}, {}={}'.format(labels[2], tanval, labels[3], A0, labels[4], sign), fontsize = 18)
	
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
	c_check = 'blue'
	ax.tricontour(xar, yar, new_zar, linewidths=lw_0, colors=c_check, linestyles='-', levels=[0.49,0.5,0.51])

	if save:
		plt.savefig('plots/{}_{}_{}.png'.format(tanval, A0_text, sign))
	return fig



##################################################################
if __name__ == "__main__":
	plot_prefix = 'cmssm'
	infile = 'data/cmssm.txt'

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
		plt.close()
		plt.clf()


