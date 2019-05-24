#!/usr/bin/python


import os
import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from itertools import chain
from matplotlib import colors
import xslha

def parse_topo(topo_file):
	processes = []
	with open(topo_file, 'r') as file:
		data = file.readlines()
		for line in data:
			if len(line)>0 and line[0]=='#':
				continue
			else:
				for proc in line.strip().split():
					if proc[0]=='(':
						if proc[-1]==')':
							processes.append((proc[1:-1], False))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append((proc[1:], False))
					elif proc[-1]==')':
						print('[WARNING] {} without starting bracket! Will try to parse anyway.'.format(proc))
						processes.append((proc[:-1], False))
					elif proc[0]=='[':
						if proc[-1]==']':
							processes.append((proc[1:-1], True))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append((proc[1:], True))
					elif proc[-1]==']':
						print('[WARNING] {} without starting bracket! Will try to parse anyway.'.format(proc))
						processes.append((proc[:-1], True))
					else:
						processes.append((str(proc), False))
	return processes					

def get_name(pid):
	ppid = pid
	if pid < 0:
		ppid = -pid
		
	if ppid == 24:
		return 'W+'
	elif ppid == 25:
		return 'h'
	elif ppid == 35:
		return 'H'
	elif ppid == 36:
		return 'A'
	elif ppid == 37:
		return 'H+'
	elif ppid == 1000001:
		return 'DL'
	elif ppid == 2000001:
		return 'DR'
	elif ppid == 1000002:
		return 'UL'
	elif ppid == 2000002:
		return 'UR'
	elif ppid == 1000003:
		return 'SL'
	elif ppid == 2000003:
		return 'SR'
	elif ppid == 1000004:
		return 'CL'
	elif ppid == 2000004:
		return 'CR'
	elif ppid == 1000005:
		return 'B1'
	elif ppid == 2000005:
		return 'B2'
	elif ppid == 1000006:
		return 'T1'
	elif ppid == 2000006:
		return 'T2'
	elif ppid == 1000011:
		return 'ER'
	elif ppid == 2000011:
		return 'EL'
	elif ppid == 1000015:
		return 'TAU1'
	elif ppid == 2000015:
		return 'TAU2'
	elif ppid == 1000021:
		return 'G'
	elif ppid == 1000022:
		return 'N1'
	elif ppid == 1000023:
		return 'N2'
	elif ppid == 1000025:
		return 'N3'
	elif ppid == 1000035:
		return 'N4'
	elif ppid == 1000024:
		return 'C1'
	elif ppid == 1000037:
		return 'C2'
	elif ppid == 13:
		return 'm'
	elif ppid in [1000012, 1000014]:
		return 'NU'
	elif ppid == 1000016:
		return "NUT"
	elif ppid == 1000039:
		return "R32"
	elif ppid == 1000013:
		return 'ML'
	elif ppid == 2000013:
		return 'MR'
	elif ppid == 11:
		return 'e'
	elif ppid == 13:
		return 'm'
	elif ppid == 15:
		return 'ta'
	elif ppid == 5:
		return 'b'
	else:
		# print('Unknown particle with pid={}'.format(pid))
		return None


def read_masses(slha_path):
	d = xslha.read(slha_path)
	mb = d.blocks['MASS']
	masses = {}
	for par in mb.items():
		name = get_name(int(par[0]))
		if name is not None:
			masses[name] = par[1]
	new_masses = {}
	for par in masses.items():
		name = str(par[0])
		if name[-1] == 'R' or name[-1] == 'L':
			new_masses[name[:-1]] = 0.5 * (masses[name[:-1] + 'R'] + masses[name[:-1] + 'L'])

	return {**masses, **new_masses}

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
		self.checked_rates = []
		self.checked_procs = []
		self.checked_xsecs = []
		self.tot_check_rate = None
		self.tot_check_xsec = None
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.top3proc = []
		self.top3rate = []
		self.top3xsec = []
		self.broken = False
		self.mass_spectrum = None
		self.name = "{m0}_{mhalf}_{tanB}_{A0}_{sign}".format(m0=self.m0, mhalf=self.mhalf, tanB=self.tanB, A0=self.A0, sign=self.sign)

	def add_data(self, proc, xsec, rate):
		self.rates.append(float(rate))
		self.procs.append(proc.strip())
		self.xsecs.append(float(xsec))

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

	def set_checked(self, exp_procs):
		sure = set([p[0] for p in exp_procs if not p[1]])
		unsure = [p[0] for p in exp_procs if p[1]]
		for proc in unsure:
			p1 = proc.split('_')[0]
			p2 = proc.split('_')[1]
			masses = []
			names = []
			for p in (p1, p2):
				if p[0] in ('G', 'Q', 'E'):
					names.append(p[0])
					if p[0] == 'Q':
						mQ = 0.0
						for pid in (range(1000001, 1000005) + range(2000001, 2000005)):
							mQ += self.mass_spectrum[get_name(pid)]
						masses.append(mQ/8.)
					else:
						masses.append(self.mass_spectrum[p[0]])
				elif p[0:2] in ('N1', 'N2', 'N3', 'N4', 'T1', 'T2', 'B1', 'B2', 'C1', 'C2'):
					names.append(p[0:2])
					masses.append(self.mass_spectrum[p[0:2]])
				elif p[0:3] == 'TAU':
					names.append(p[0:4])
					masses.append(self.mass_spectrum[p[0:4]])
			assert len(masses)==2, 'There should be 2 masses for unsure checked processes!'
			val = abs(masses[0]-masses[1])/min(masses)
			if val < 0.1:
				sure.add(proc)
			else:
				print(proc)

		indices = [ii for ii, proc in enumerate(self.procs) if proc in sure]
		for ii in indices:
			self.checked_procs.append(self.procs[ii])
			self.checked_rates.append(self.rates[ii])
			self.checked_xsecs.append(self.xsecs[ii])
		self.tot_checked_xsec = sum(self.checked_xsecs)
		self.tot_checked_rate = sum(self.checked_rates)

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


def plot_rate_xsec(points, cdata='tot_checked_'):
	# we define a subfunction for plotting A0
	def make_plot(data, tanval, A0val, signvalm, text_short, text_long, limits, cdata):
		# Select what kind of data to plot, 'max' will plot the coverage/xsec of the top process, 'tot_checked_' will plot what experiments test.
		if cdata == 'max':
			title = 'Top'
		elif cdata == 'tot_checked_':
			title = 'Total'
		else:
			print('Wrong cdata argument for plot function, it has to be \"max\" or \"tot_checked_\"" !')
			exit(1)
		# Small differences in plots for xsection and rate
		if text_short == 'rate':
			vmax = 100
			norm = colors.Normalize(vmin=0.,vmax=vmax)
			unit = ''
		else:
			vmax = max(data['{}{}'.format(cdata, text_short)])
			norm = colors.LogNorm()
			unit='/fb'
		# Create figures and plots
		cmap = cm.get_cmap('gist_rainbow_r') # Colour map (there are many others)
		# plot rate for A0 = 0
		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0 [GeV/c^2]$', fontsize=14)
		ax.yaxis.set_label_text(r'$m_{1/2} [GeV/c^2]$', fontsize=14)
		plt.title(r"{title} {text} for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(title=title, sign=signval, tan=tanval, A0=A0val, text=text_long), fontsize=14, loc='left')
		sc = ax.scatter(data['m0'].tolist(), data['mhalf'].tolist(), c=data['{}{}'.format(cdata, text_short)].tolist(), s=200, cmap=cmap,\
		 edgecolor='face', marker='s', vmin=10.**-1, vmax=vmax, norm=norm)
		cb = plt.colorbar(sc, shrink=0.9)
		cb.ax.set_title(text_short+unit, fontsize=10)
		plt.xlim(limits[0], limits[1])
		if '$' in A0val:
			A0val = '-mhalf'
		fig.subplots_adjust(left=0.15, right=0.99, top=0.85, bottom=0.15)
		plt.savefig("plots/{text}/{title}_{text}_{}_{}_{}.png".format( tanval, A0val, signval, title=title, text=text_short))
		plt.close()

	# Select data for plotting
	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'tot_checked_rate', 'tot_checked_xsec', 'maxrate', 'maxxsec']
	df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in points])
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	# Iterate over four groups (2 vals of tanBeta and signMu)
	for gr in groups:
		gr=gr.apply(pd.to_numeric)
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		# Two cases for A0, it's either 0 or -mhalf
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]
		make_plot(zeroA0, tanval, '0', signval, 'rate', 'coverage', (0, 3100), cdata=cdata)
		make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'rate', 'coverage', (0, 3100), cdata=cdata)
		make_plot(zeroA0, tanval, '0', signval, 'xsec', 'cross-section', (0, 3100), cdata=cdata)
		make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'xsec', 'cross-section', (0, 3100), cdata=cdata)
		

		


def main(in_path, slha_path=None):
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
			# read mass block from slha if possible
			try:
				spectrum = read_masses(os.path.join(slha_path, name+'.slha'))
				points[-1].mass_spectrum = spectrum
			except IOError as e:
				print('[WARNING] Could not load masses from slha file: {} !'.format(name))
	print('Points loaded!')
	# load topologies checked by ATLAS & CMS
	checked_procs = parse_topo('topologies.txt')
	print('Topologies loaded!')
	# remove broken files without the process list
	points = [p for p in points if p.broken == False]
	# find out contribution from processes studied by ATLAS and CMS
	for p in points:
		p.set_checked(checked_procs)
	return points, broken_files

if __name__ == '__main__':
	in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
	slha_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
	if len(sys.argv) == 2:
		in_path = str(sys.argv[1])
	elif len(sys.argv) == 3:
		in_path = str(sys.argv[1])
		slha_path = str(sys.argv[1])

	points, broken_files = main(in_path, slha_path)
	# plot results
	plot_rate_xsec(points)
	# plot_rate_xsec(points, checked_procs, cdata='max')
	plot_hist(points)

	# print(points[-1].mass_spectrum)

	with open('broken_files.txt', 'w') as bf:
		bf.write('\n'.join(broken_files))




