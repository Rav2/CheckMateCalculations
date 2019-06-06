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
from matplotlib.table import Cell
import xslha
import copy
from matplotlib.font_manager import FontProperties
from matplotlib.text import Annotation, Text
class Point:
	def __init__(self, m0, mhalf, tanB, A0, sign):
		self.m0 = m0
		self.mhalf = mhalf
		self.tanB = tanB
		self.A0 = A0
		self.sign = sign
		self.top_group = ''
		self.procs = []
		self.errors = []
		self.allowed_procs = []
		self.tot_check_rate = None
		self.tot_check_xsec = None
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.top3proc = []
		self.broken = False
		self.mass_spectrum = None
		self.name = "{m0}_{mhalf}_{tanB}_{A0}_{sign}".format(m0=self.m0, mhalf=self.mhalf, tanB=self.tanB, A0=self.A0, sign=self.sign)

	def add_data(self, proc, xsec, rate):
		self.procs.append(Process(proc.strip(), xsec, rate, False))

	def set_tops(self):
		if len(self.procs) == 0:
			self.maxxsec = 0.0
			self.maxrate = 0.0
			return
		self.allowed_procs.sort(key=lambda x: x.rate, reverse=True)
		self.maxproc = self.allowed_procs[0].proc
		self.maxrate = self.allowed_procs[0].rate
		self.maxxsec = self.allowed_procs[0].xsec
		self.top_group = self.allowed_procs[0].group
		for ii in range(0, min(3, len(self.allowed_procs))):
			self.top3proc.append(self.allowed_procs[ii].proc)

	def set_allowed(self, topo):
		allowed = {}
		# extract topologies that are allowed
		topo_copy = copy.deepcopy(topo)
		for proc in topo_copy:
			proc.analyze_process(self.mass_spectrum)
			if proc.allowed:
				allowed[proc.proc] = proc.brackets
		# get indices of processes in self.proc that should be allowed
		indices = [ii for ii, proc in enumerate(self.procs) if proc.proc in allowed.keys()]
		for ii in indices:
			self.procs[ii].brackets = allowed[self.procs[ii].proc]
			self.procs[ii].analyze_process(self.mass_spectrum)
			self.allowed_procs.append(self.procs[ii])
			# self.allowed_procs[-1].analyze_process(self.mass_spectrum)
		self.tot_allowed_xsec = sum([a.xsec for a in self.allowed_procs])
		self.tot_allowed_rate = sum([a.rate for a in self.allowed_procs])

	def add_err(self, msg):
		self.errors.append(msg)

	def get_proc_no(self):
		return len(self.procs)

	def is_broken(self):
		self.broken = True

	def limit_to_group(self, group, topo):
		self.allowed_procs = []
		self.tot_check_rate = None
		self.tot_check_xsec = None
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.top3proc = []
		self.tot_allowed_xsec = 10.0**-20
		self.tot_allowed_rate = 10.0**-20
		self.top_group = None
		processes = [p for p in self.procs if p.group == group]
		self.procs = processes
		if len(self.procs) > 0:
			self.set_allowed(topo)
			self.set_tops()
		else:
			self.top_group = 'no_data'


class Process():
	def __init__(self, proc, xsec, rate, brackets=False):
		self.proc = proc
		self.xsec = xsec
		self.rate = rate
		self.init_pars = None
		self.SM_pars = None
		self.SUSY_pars = None
		self.brackets = brackets
		self.allowed = False
		self.group = None

	def detectGroup(self):
		if self.SM_pars is None:
			raise Exception('First anlyze the processes, then detect group!')
		else:

			if self.init_pars[0] == self.init_pars[1]:
				if self.init_pars[0] == 'G':
					if len(self.SUSY_pars[0]+self.SUSY_pars[1]) >= 2 and self.SUSY_pars[0][0] in ('T1', 'T2', 'B1', 'B2') and self.SUSY_pars[1][0] in ('T1', 'T2', 'B1', 'B2'):
						self.group = 'G(G->stop)'
					elif len(self.SUSY_pars[0]+self.SUSY_pars[1]) == 0 and all([x in ('b','t','q') for x in self.SM_pars]):
						self.group = 'G(G->quark)'
					elif len(self.SUSY_pars[0]+self.SUSY_pars[1]) == 0 and self.SM_pars.count('g') == 1:
						self.group = 'G(G->g)'
					else:
						self.group = 'G(G->other)'
				elif self.init_pars[0] in ('T1', 'T2', 'B1', 'B2'):
					if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
						self.group = 'T(T->N1)'
					else:
						self.group = 'T(T->other)'
				elif self.init_pars[0] == 'Q':
					if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
						self.group = 'Q(Q->N1)'
					elif len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and len(self.SUSY_pars[1]) == 1 and \
									self.SUSY_pars[0][0][0] in ('N', 'C') and self.SUSY_pars[1][0][0] in ('N', 'C'):
						self.group = 'Q(Q->X)'
					else:
						self.group = 'Q(Q->other)'
				elif self.init_pars[0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT'):
					if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
						self.group = 'SL(SL->N1)'
					else:
						self.group = 'SL(SL->other)'
				else:
					self.group = 'other'
			else:
				if self.init_pars[0][0] in ('C', 'N') and self.init_pars[1][0] in ('C', 'N'):
					if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
						self.group = 'X(X->N1)'
					elif len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and len(self.SUSY_pars[1]) == 1 and \
									self.SUSY_pars[0][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT') and \
									self.SUSY_pars[1][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT'):
						self.group = 'X(X->SL)'
					else:
						self.group = 'X(X->other)'
				else:
					self.group = 'other'


	def analyze_process(self, masses, omit_mass_check=False):
		SM1 = ('q', 'e', 'b', 't', 'g', 'z', 'h', 'w', 'n', 'm')
		SM2 = ('ta', 'nu')
		SM = SM1+SM2
		SUSY1 = ('G', 'Q', 'E', 'M')
		SUSY2 = ('N1', 'N2', 'N3', 'N4', 'T1', 'T2', 'B1', 'B2', 'C1', 'C2', 'NU')
		SUSY3 = ('NUT')
		SUSY4 = ('TAU1', 'TAU2')
		SUSY = SUSY1 + SUSY2 + SUSY4

		br1 = self.proc.split('_')[0]
		br2 = self.proc.split('_')[1]
		sm_pars = []
		susy_pars = []
		# extract particles from the string
		for br in (br1, br2):
			susys = []
			for ii, char in enumerate(br):
				if ii >= len(br):
					break

				if char.isupper():
					if len(br[ii:])>3 and br[ii:ii+4] in SUSY:
						susys.append(br[ii:ii+4])
						ii = ii+4
					elif len(br[ii:])>2 and br[ii:ii+3] in SUSY:
						susys.append(br[ii:ii+3])
						ii = ii+3
					elif len(br[ii:])>1 and br[ii:ii+2] in SUSY:
						susys.append(br[ii:ii+2])
						ii = ii+2
					elif char in SUSY:
						susys.append(char)
				else:
					if len(br[ii:])>1 and br[ii:ii+2] in SM:
						sm_pars.append(br[ii:ii+2])
						ii = ii+2
					elif char in SM:
						sm_pars.append(char)
			susy_pars.append(susys)
		# write found particles to fields
		self.init_pars = (susy_pars[0][0], susy_pars[1][0])
		self.SM_pars = tuple(sm_pars)
		self.SUSY_pars = (susy_pars[0][1:-1], susy_pars[1][1:-1])
		tot_no_of_SUSY_pars = len(set(susy_pars[0] + susy_pars[1]))
		# parse brackets == check for masses
		if self.brackets and len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and not omit_mass_check:
			ew_pars =  ('C1', 'C2', 'N1', 'N2', 'N3', 'N4')
			stops = ('T1', 'T2', 'B1', 'B2')

			for p1, p2 in zip(susy_pars[0][1:-1], susy_pars[1][1:-1]):
				m1 = masses[p1]
				m2 = masses[p2]
				if p1 != p2 and ((p1 in ew_pars and p2 in ew_pars) or (p1 in stops and p2 in stops)) and abs(m1-m2)/min((m1, m2)) < 0.1:
					tot_no_of_SUSY_pars -= 1
		# we discard processes that require more than 3 SUSY masses
		if tot_no_of_SUSY_pars < 4:
			self.allowed = True
			# set topological groups
			self.detectGroup()
		else:
			self.allowed = False

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
							processes.append(Process(proc[1:-1], 0., 0., False))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append(Process(proc[1:], 0., 0., False))
					elif proc[-1]==')':
						print('[WARNING] {} without starting bracket! Will try to parse anyway.'.format(proc))
						processes.append(Process(proc[:-1], 0., 0., False))
					elif proc[0]=='[':
						if proc[-1]==']':
							processes.append(Process(proc[1:-1], 0., 0., True))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append(Process(proc[1:], 0., 0., True))
					elif proc[-1]==']':
						print('[WARNING] {} without starting bracket! Will try to parse anyway.'.format(proc))
						processes.append(Process(proc[:-1], 0., 0., True))
					else:
						processes.append(Process(str(proc), 0., 0., False))
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
			masses[name] = abs(par[1])
	# now deal with R,L chiralities
	new_masses = {}
	for par in masses.items():
		name = str(par[0])
		if name[-1] == 'R' or name[-1] == 'L':
			m = 0.5 * (masses[name[:-1] + 'R'] + masses[name[:-1] + 'L'])
			if name[0] != 'N':
				assert m>0, 'Mass of {} should be >0'.format(name)
			new_masses[name[:-1]] = abs(m)
	new_masses['Q'] = 1./4.*(new_masses['U']+new_masses['D']+new_masses['S']+new_masses['C'])
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



def plot_hist(points):
	maxprocs = [p.maxproc for p in points]
	proc_counts = Counter(maxprocs)
	plot_bar_from_counter(proc_counts.most_common(10))
	# plt.xticks(rotation=90)
	plt.title('Top process occurence (10 highest results)')
	if not os.path.exists('plots/!proc'):
		os.mkdir('plots/!proc')
	plt.savefig('plots/!proc/top_process.png')

	plt.clf()
	top3 = [p.top3proc for p in points]
	top3 = list(chain.from_iterable(top3))
	top3_counts = Counter(top3)
	plot_bar_from_counter(top3_counts.most_common(15))
	# plt.xticks(rotation=90)
	plt.title('Top 3 processes occurence (15 highest results)')
	plt.savefig('plots/!proc/top3_process.png')


def plot_rate_xsec(points, cdata='tot_allowed_', folder='', group_names = None):
	# we define a subfunction for plotting A0
	def make_plot(data, tanval, A0val, signvalm, text_short, text_long, limits, cdata, folder, group_names = None):
		# Select what kind of data to plot, 'max' will plot the coverage/xsec of the top process, 'tot_allowed_' will plot what experiments test.
		if cdata == 'max':
			title = 'Top'
		elif cdata == 'tot_allowed_':
			title = 'Total'
		else:
			print('Wrong cdata argument for plot function, it has to be \"max\" or \"tot_allowed_\"" !')
			exit(1)

		# Small differences in plots for xsection and rate
		if text_short == 'rate':
			if folder == '':
				vmax = 100
			else:
				vmax = max(data['{}{}'.format(cdata, text_short)].tolist())
			norm = colors.Normalize(vmin=0.,vmax=vmax)
			unit = ''
		else:
			vmax = max(data['{}{}'.format(cdata, text_short)].tolist())
			norm = colors.LogNorm()
			unit='/fb'

		# Create figures and plots
		cmap = cm.get_cmap('gist_rainbow_r') # Colour map (there are many others)

		fig, ax = plt.subplots(1)
		ax.xaxis.set_label_text(r'$m_0 [GeV/c^2]$', fontsize=14)
		ax.yaxis.set_label_text(r'$m_{1/2} [GeV/c^2]$', fontsize=14)
		plt.title(r"{title} {text} for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(title=title, sign=signval, tan=tanval, A0=A0val, text=text_long), fontsize=14, loc='left')
		sc = ax.scatter(data['m0'].tolist(), data['mhalf'].tolist(), c=data['{}{}'.format(cdata, text_short)].tolist(), s=190, cmap=cmap,\
		 edgecolor='face', marker='s', alpha=0.75, vmin=10.**-1, vmax=vmax, norm=norm)
		cb = plt.colorbar(sc, shrink=0.9)
		cb.ax.set_title(text_short+unit, fontsize=10)
		plt.xlim(limits[0], limits[1])
		plt.ylim(0.85*min(data['mhalf'].tolist()), 1.05*max(data['mhalf'].tolist()))

		if '$' in A0val:
			A0val = '-mhalf'

		if folder is not None and folder != '':
			text = folder
		else:
			text = '!'+text_short

		if not os.path.exists('plots/' + text):
			os.mkdir('plots/' + text)
		# Deal with groups
		group_leg = 'Dominant topology:'
		if group_names is not None:
			group_dict ={}
			for ii, gg in enumerate(sorted(group_names)):
				group_leg += '\n'+ str(ii)+' '+gg
				group_dict[gg] = ii
			# top_g = data['top_group'].to_list()
			# print numbers on points
			for index, row in data[['m0','mhalf','top_group']].iterrows():
				try:
					# there might no processes belonging to certain group
					if row['top_group'] == 'no_data':
						plt.text(row['m0'] - 45, row['mhalf'] - 25, 'X', fontsize=14, fontweight='bold')
					else:
						plt.text(row['m0']-45, row['mhalf']-25, group_dict[row['top_group']], fontsize=12)
				except KeyError:
					print(row['m0'], row['mhalf'])
					dejta = data[index:index+1]
					pass
			# print group legend
			props = dict(boxstyle='round', facecolor='wheat', alpha=0.2)
			plt.gcf().text(0.01, 0.99, group_leg,  fontsize=10, verticalalignment='top', bbox=props)
			fig.subplots_adjust(left=0.25, right=0.99, top=0.85, bottom=0.15)
		else:
			fig.subplots_adjust(left=0.15, right=0.99, top=0.85, bottom=0.15)

		plt.savefig("plots/{text}/{title}_{stext}_{}_{}_{}.png".format( tanval, A0val, signval, title=title, text=text, stext=text_short))
		plt.close()

	# Select data for plotting
	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'tot_allowed_rate', 'tot_allowed_xsec', 'maxrate', 'maxxsec', 'top_group']
	df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in points])
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	# Iterate over four groups (2 vals of tanBeta and signMu)
	for gr in groups:
		gr[fields[:-1]] = gr[fields[:-1]].apply(pd.to_numeric)
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		# Two cases for A0, it's either 0 or -mhalf
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]
		if not zeroA0.empty:
			make_plot(zeroA0, tanval, '0', signval, 'rate', 'coverage', (0, 3150), cdata=cdata, folder=folder, group_names=group_names)
			make_plot(zeroA0, tanval, '0', signval, 'xsec', 'cross-section', (0, 3150), cdata=cdata, folder=folder)
		if not nonzeroA0.empty:
			make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'rate', 'coverage', (0, 3150), cdata=cdata, folder=folder, group_names=group_names)
			make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'xsec', 'cross-section', (0, 3150), cdata=cdata, folder=folder)


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
			# read mass block from slha if possible
			try:
				spectrum = read_masses(os.path.join(slha_path, name+'.slha'))
				points[-1].mass_spectrum = spectrum
			except IOError as e:
				print('[WARNING] Could not load masses from slha file: {} !'.format(name))

	print('Points loaded!')
	# load topologies allowed by ATLAS & CMS
	topos = parse_topo('topologies.txt')
	print('Topologies loaded!')
	# remove broken files without the process list
	points = [p for p in points if p.broken == False]
	# find out contribution from processes studied by ATLAS and CMS
	for p in points:
		p.set_allowed(topos)
		p.set_tops()
		if p.name == '514_514_5_-514_-1':
			print('O KURWA!')
	return points, broken_files, topos

if __name__ == '__main__':
	in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
	slha_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
	if len(sys.argv) == 2:
		in_path = str(sys.argv[1])
	elif len(sys.argv) == 3:
		in_path = str(sys.argv[1])
		slha_path = str(sys.argv[1])

	points, broken_files, topo = main(in_path, slha_path)

	print('Detecting groups!')
	groups = []
	for point in points:
		for proc in point.allowed_procs:
			if proc.group is not None:
				groups.append(proc.group)
	# groups.append('no_data')
	groups = set(groups)
	print(groups)

	print('Plotting basic plots!')
	plot_rate_xsec(points, group_names=tuple(groups))
	plot_hist(points)

	for gg in groups:
		grouped = copy.deepcopy(points)
		for point in grouped:
			point.limit_to_group(gg, topo)
		if len(grouped) > 0:
			plot_rate_xsec(grouped, folder=gg.replace('(','').replace(')',''), group_names=tuple(groups))

	with open('broken_files.txt', 'w') as bf:
		bf.write('\n'.join(broken_files))




