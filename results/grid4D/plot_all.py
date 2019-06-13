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

def do_plot(x, y, z, val, r, labels, mode='G'):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# plt.rc('font', family='Helvetica')

	# defining color map
	# vals = [(0,"darkcyan"), (0.10,"green"), (0.20,"lime"), (0.30,"limegreen"), (0.40,"palegreen"),
	# (0.60, "salmon"), (0.70, "tomato"), (0.80, "red"), (0.9, "maroon"), (1, "sienna")]
	
	# colors in total
	colors1 = plt.cm.hot(np.linspace(0.6, 0.1, 128))
	colors2 = plt.cm.summer(np.linspace(0.0, 0.6, 128))

	# combine them and build a new colormap
	colors = np.vstack((colors2, colors1))
	mymap = cls.LinearSegmentedColormap.from_list('my_colormap', colors)



	# scatter plot #nipy_spectral
	vmin, vmax = 10**-2, 100
	sc = ax.scatter(x, y, z, c=r, cmap=mymap, norm=cls.LogNorm(), 
		vmin=vmin, vmax=vmax, lw=0.5, edgecolors='black', marker='o', s=50, alpha=0.7, rasterized=False)   

	fig.subplots_adjust(bottom=0.08, right=0.90, top=0.95, left=0.10)
	# ticks and limit
	ax.xaxis.set_ticks(np.arange(1000, 3001, 500))
	ax.set_xlim(950, 3050)
	ax.yaxis.set_ticks(np.arange(500, 3001, 500))
	ax.set_ylim(450,3050)
	if mode=='G':
		# mG is used to slice
		ax.zaxis.set_ticks(np.arange(1, 3001, 500))
		ax.set_zlim(1,3050)
	else:
		# mN1 is used to slice		
		ax.zaxis.set_ticks(np.arange(1000, 3001, 500))
		ax.set_zlim(950,3050)

	# axes labels
	ax.set_xlabel(labels[0]+r'$ [\rm GeV/c^2]$', fontsize=18, labelpad=12, fontname='Helvetica')
	ax.set_ylabel(labels[1]+r'$ [\rm GeV/c^2]$', fontsize=18, labelpad=12, fontname='Helvetica')
	ax.set_zlabel(labels[2]+r'$ [\rm GeV/c^2]$', fontsize=18, labelpad=12, fontname='Helvetica')

	
	# color bar
	cbaxes = fig.add_axes([0.10, 0.1, 0.03, 0.8]) 
	cb = plt.colorbar(sc, pad=0.05, shrink=0.8, cax=cbaxes, orientation='vertical', cmap=mymap)#, ticks=[10**-2, 10**-1, 1, 10, 100], boundaries=[10**-2, 1, 100])
	# cb.ax.set_yticklabels([10**-2, 10**-1, 1, 10, 100])
	cbaxes.yaxis.set_ticks_position('left')

	# text box
	textstr = labels[-1] + '={}'.format(int(val)) + r'$ [\rm GeV/c^2]$'
	# these are matplotlib.patch.Patch properties
	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	# place a text box in upper left in axes coords
	ax.text2D(0.10, 0.97, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props, fontname='Helvetica')

	if mode=='G':
		plt.savefig("plots/G_slice/G_{}.png".format(val))
	else:
		plt.savefig("plots/N1_slice/N1_{}.png".format(val))
	plt.close()

##################################################################

plot_prefix = 'minigrid'
infile = 'collective_results.txt'

labelsG = [r'$m_Q$', r'$m_{Q_3}$', r'$m_{\chi^0_1}$', r'$m_G$']
labels2G = ['Q', 'Q3', 'N1', 'G']
labelsN = [r'$m_Q$', r'$m_{Q_3}$', r'$m_G$', r'$m_{\chi^0_1}$']
labels2N = ['Q', 'Q3', 'G', 'N1']

# load data
data_raw = np.loadtxt(infile, skiprows=2, usecols=range(0,5))
data = data_raw.transpose()
assert len(labelsG)+1 == len(data), "Labels not set!" 
assert len(labelsN)+1 == len(data), "Labels not set!" 

# plot with mG slices
df=pd.DataFrame(data_raw).sort_values(0)
groups = df.groupby(0)
group_names = df[0].unique()
for name in group_names:
	x = []
	y = []
	z = []
	r = []
	val = name
	for index, row in groups.get_group(name).iterrows():
		x.append(row[1])
		y.append(row[2])
		z.append(row[3])
		r.append(row[4])
	do_plot(x, y, z, val, r, labelsG, 'G')

# plot with mN1 slices
#df=pd.DataFrame(data_raw).sort_values(3)
#groups = df.groupby(3)
#group_names = df[3].unique()
#for name in group_names:
#	x = []
#	y = []
#	z = []
#	r = []
#	val = name
#	for index, row in groups.get_group(name).iterrows():
#		x.append(row[1])
#		y.append(row[2])
#		z.append(row[0])
#		r.append(row[4])
#	do_plot(x, y, z, val, r, labelsN, 'N')
