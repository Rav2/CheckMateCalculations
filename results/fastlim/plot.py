#!/usr/bin/python


import os
import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def plot_bar_from_counter(counter, ax=None):
    """"
    This function creates a bar plot from a counter.

    :param counter: This is a counter object, a dictionary with the item as the key
     and the frequency as the value
    :param ax: an axis of matplotlib
    :return: the axis wit the object in it
    """

    if ax is None:
        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(111)

    frequencies = [f[1] for f in counter]
    names = [f[0] for f in counter]

    x_coordinates = np.arange(len(counter))
    ax.bar(x_coordinates, frequencies, align='center')

    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
    ax.xaxis.set_tick_params(labelsize=10)
    ax.set_ylim(0, 1120)
    for i, v in enumerate(frequencies):
    	ax.text(i-0.25, v + 7, str(v), color='black', fontweight='bold')

    fig.subplots_adjust(bottom=0.45)
    return ax

class Point:
	def __init__(self, m0, mhalf, tanB, A0, sign, maxproc, maxxsec, maxrate):
		self.m0 = m0
		self.mhalf = mhalf
		self.tanB = tanB
		self.A0 = A0
		self.sign = sign
		self.maxrate = maxrate
		self.maxproc = maxproc
		self.maxxsec = maxxsec
		pp = maxproc.split('_')
		if pp[0][0] in ['C', 'N', 'T', 'B']:
			p1 = pp[0][:2]
		else:
			p1 = pp[0][0]
		if pp[1][0] in ['C', 'N', 'T', 'B']:
			p2 = pp[1][:2]
		else:
			p2 = pp[1][0]
		self.mode = p1 + '_' + p2

def plot_hist(points):
	maxprocs = [p.maxproc for p in points]
	proc_counts = Counter(maxprocs)
	plot_bar_from_counter(proc_counts.most_common())
	plt.xticks(rotation=90)
	plt.title('Top process occurence')
	plt.savefig('plots/top_process.png')

def plot_rate(points):
	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'maxrate', 'maxxsec']
	df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in points])
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	for gr in groups:
		gr[["m0", "mhalf", "A0", "tanB", "sign", "maxrate", "maxxsec"]] = gr[["m0", "mhalf", "A0", "tanB", "sign", "maxrate", "maxxsec"]].apply(pd.to_numeric)
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]

		cmap = cm.get_cmap('hsv') # Colour map (there are many others)
		
		# plot rate for A0 = 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Rate for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=0))
		sc = ax.scatter(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), c=zeroA0['maxrate'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s', vmin=0., vmax=100.)
		plt.colorbar(sc)
		plt.xlim(750, 3050)
		plt.savefig("plots/rate_{}_{}_{}.png".format(tanval, 0, signval))
		plt.close()
		
		# plot rate for A0 != 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Rate for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=r'$-m_{1/2}$'))
		sc = ax.scatter(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), c=nonzeroA0['maxrate'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s', vmin=0., vmax=100.)
		plt.colorbar(sc)
		plt.xlim(750, 3050)
		plt.savefig("plots/rate_{}_{}_{}.png".format(tanval, '-mhalf', signval))	
		plt.close()	

		# plot xsec for A0 = 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"x-sec for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=0))
		sc = ax.scatter(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), c=zeroA0['maxxsec'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s')
		plt.colorbar(sc)
		plt.xlim(750, 3050)
		plt.savefig("plots/xsec{}_{}_{}.png".format(tanval, 0, signval))
		plt.close()
		
		# plot xsec for A0 != 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"x-sec for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=r'$-m_{1/2}$'))
		sc = ax.scatter(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), c=nonzeroA0['maxxsec'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s')
		plt.colorbar(sc)
		plt.xlim(750, 3050)
		plt.savefig("plots/xsec{}_{}_{}.png".format(tanval, '-mhalf', signval))	
		plt.close()	

def main(in_path):
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(in_path):
	    for file in f:
	    	files.append(os.path.join(r, file))

	broken_files = []
	points = []
	for file in files:
	    with open(file, 'r') as f:
	    	fileOK = True
	    	content = f.readlines()
	    	for ii,line in enumerate(content):
	    		if "Output upto" in line:
	    			res = content[ii+2]
	    			proc = res.strip().split(':')[0]
	    			xsec = float(res.strip().split(':')[1].strip().split()[0])
	    			rate = float(res.strip().split(':')[1].strip().split()[1].strip()[1:-2])
	    			name = str(file.split('/')[-1].split('.')[0])
	    			name_arr = name.split('_')[1:]
	    			assert(len(name_arr) == 5)
	    			points.append(Point(name_arr[0], name_arr[1], name_arr[2], name_arr[3], name_arr[4], proc, xsec, rate))
	    		else:
	    			broken_files.append(file)

	plot_hist(points)   			
	plot_rate(points)

	with open('broken_files.txt', 'w') as bf:
		bf.write('\n'.join(broken_files))

if __name__ == '__main__':
	in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
	if len(sys.argv) == 2:
		in_path = str(sys.argv[1])
	main(in_path)



