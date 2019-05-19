#!/usr/bin/python


import os
import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from itertools import chain
def plot_bar_from_counter(counter, ax=None):
	""""
	This function creates a bar plot from a counter.

	:param counter: This is a counter object, a dictionary with the item as the key
	 and the frequency as the value
	:param ax: an axis of matplotlib
	:return: the axis wit the object in it
	"""

	if ax is None:
		fig = plt.figure(figsize=(7,5))
		ax = fig.add_subplot(111)

	frequencies = [f[1] for f in counter]
	names = [f[0] for f in counter]

	x_coordinates = np.arange(len(counter))
	ax.barh(x_coordinates, frequencies, align='center')

	ax.yaxis.set_major_locator(plt.FixedLocator(x_coordinates))
	ax.yaxis.set_major_formatter(plt.FixedFormatter(names))
	ax.yaxis.set_tick_params(labelsize=10)
	ax.set_ylim(-1, len(counter)+1)
	ax.set_xlim(0, max(frequencies)+300)
	for i, v in enumerate(frequencies):
		ax.text( v + 20, i-0.25, str(v), color='black', fontweight='normal', fontsize=10)

	fig.subplots_adjust(left=0.4)
	return ax

class Point:
	def __init__(self, m0, mhalf, tanB, A0, sign):
		self.m0 = m0
		self.mhalf = mhalf
		self.tanB = tanB
		self.A0 = A0
		self.sign = sign
		self.rates = []
		self.procs = []
		self.xsecs = []
		self.errors = []
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.top3proc = []
		self.top3rate = []
		self.top3xsec = []
		self.broken = False
		self.name = "{m0}_{mhalf}_{tanB}_{A0}_{sign}".format(m0=self.m0, mhalf=self.mhalf, tanB=self.tanB, A0=self.A0, sign=self.sign)

	def add_data(self, proc, xsec, rate):
		self.rates.append(rate)
		self.procs.append(proc)
		self.xsecs.append(xsec)

	def set_tops(self):
		assert (len(self.rates) == len(self.procs) and len(self.procs) == len(self.xsecs))
		assert(len(self.procs) > 0)
		self.maxrate = self.rates[0]
		self.maxproc = self.procs[0]
		self.maxxsec = self.xsecs[0]
		pp = self.maxproc.split('_')
		if pp[0][0] in ['C', 'N', 'T', 'B']:
			p1 = pp[0][:2]
		else:
			p1 = pp[0][0]
		if pp[1][0] in ['C', 'N', 'T', 'B']:
			p2 = pp[1][:2]
		else:
			p2 = pp[1][0]
		self.mode = p1 + '_' + p2
		for ii in range(0, min(3, len(self.procs))):
			self.top3proc.append(self.procs[ii])
			self.top3rate.append(self.rates[ii])
			self.top3xsec.append(self.xsecs[ii])

	def add_err(self, msg):
		self.errors.append(msg)

	def get_proc_no(self):
		return len(self.procs)

	def is_broken(self):
		self.broken = True

def plot_hist(points):
	maxprocs = [p.maxproc for p in points]
	proc_counts = Counter(maxprocs)
	plot_bar_from_counter(proc_counts.most_common(10))
	# plt.xticks(rotation=90)
	plt.title('Top process occurence (10 highest results)')
	plt.savefig('plots/proc/top_process.png')

	plt.clf()
	top3 = [p.top3proc for p in points]
	top3 = list(chain.from_iterable(top3))
	top3_counts = Counter(top3)
	plot_bar_from_counter(top3_counts.most_common(15))
	# plt.xticks(rotation=90)
	plt.title('Top 3 processes occurence (15 highest results)')
	plt.savefig('plots/proc/top3_process.png')


def plot_rate_xsec(points):
	#TODO:podzielic i zrobic moze dla top3
	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'maxrate', 'maxxsec']
	df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in points])
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	for gr in groups:
		gr=gr.apply(pd.to_numeric)
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]
		cmap = cm.get_cmap('gist_rainbow_r') # Colour map (there are many others)

		# plot rate for A0 = 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Top coverage for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=0))
		sc = ax.scatter(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), c=zeroA0['maxrate'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s', vmin=0., vmax=100.)
		plt.colorbar(sc)
		plt.xlim(0, 3100)
		plt.savefig("plots/rate/rate_{}_{}_{}.png".format(tanval, 0, signval))
		plt.close()
		
		# plot rate for A0 != 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Top coverage for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=r'$-m_{1/2}$'))
		sc = ax.scatter(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), c=nonzeroA0['maxrate'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s', vmin=0., vmax=100.)
		plt.colorbar(sc)
		plt.xlim(0, 3100)
		plt.savefig("plots/rate/rate_{}_{}_{}.png".format(tanval, '-mhalf', signval))
		plt.close()	

		# plot xsec for A0 = 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Top x-sec for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=0))
		sc = ax.scatter(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), c=zeroA0['maxxsec'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s')
		plt.colorbar(sc)
		plt.xlim(0, 3100)
		plt.savefig("plots/xsec/xsec{}_{}_{}.png".format(tanval, 0, signval))
		plt.close()
		
		# plot xsec for A0 != 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0$', fontsize=18)
		ax.yaxis.set_label_text(r'$m_{1/2}$', fontsize=18)
		plt.title(r"Top x-sec for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval, tan=tanval, A0=r'$-m_{1/2}$'))
		sc = ax.scatter(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), c=nonzeroA0['maxxsec'].tolist(), s=200, cmap=cmap, edgecolor='face', marker='s')
		plt.colorbar(sc)
		plt.xlim(0, 3100)
		plt.savefig("plots/xsec/xsec{}_{}_{}.png".format(tanval, '-mhalf', signval))
		plt.close()	



def main(in_path):
	prefix = 'cmssm'
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(in_path):
		for file in f:
			files.append(os.path.join(r, file))
	broken_files = []
	points = []
	for file in files:
		if len(file.split('/')[-1]) < 5 or (file.split('/')[-1])[:5] != prefix:
			print('[WARNING] Omitting {} because of wrong prefix!'.format(file.split('/')[-1]))
			continue
		with open(file, 'r') as f:
			content = f.readlines()
			name = str(file.split('/')[-1].split('.')[0])
			name_arr = name.split('_')[1:]
			assert(len(name_arr) == 5)
			points.append(Point(name_arr[0], name_arr[1], name_arr[2], name_arr[3], name_arr[4]))
			for ii,line in enumerate(content):
				if 'ERROR' in line:
					try:
						msg = str(content[ii+1]).strip()
					except Exception as e:
						msg = str(content[ii]).strip()
					points[-1].add_err(msg)
					points[-1].is_broken()
				elif "Output upto" in line:
					jj = 2
					# read process table
					while '---' not in content[ii+jj]:
						res = content[ii + jj]
						proc = res.strip().split(':')[0]
						xsec = float(res.strip().split(':')[1].strip().split()[0])
						rate = float(res.strip().split(':')[1].strip().split()[1].strip()[1:-2])
						points[-1].add_data(proc, xsec, rate)
						jj += 1
			# check if point has any processes
			if points[-1].get_proc_no() == 0:
				broken_files.append(file)
				points[-1].is_broken()
			else:
				points[-1].set_tops()
	# remove broken files without the process list
	points = [p for p in points if p.broken == False]
	plot_hist(points)   			
	plot_rate_xsec(points)

	with open('broken_files.txt', 'w') as bf:
		bf.write('\n'.join(broken_files))

if __name__ == '__main__':
	in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
	if len(sys.argv) == 2:
		in_path = str(sys.argv[1])
	main(in_path)



