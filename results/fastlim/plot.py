#!/usr/bin/python

import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from itertools import chain
from matplotlib import colors
from matplotlib.table import Cell
from matplotlib.font_manager import FontProperties
from matplotlib.text import Annotation, Text
from cmssm import Point, Process
from utilities import *
import itertools
from collections import OrderedDict
import operator

#matplotlib.use('Agg')

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

	# for discarded processes
	disc_maxprocs = [p.disc_maxproc for p in points]
	disc_proc_counts = Counter(disc_maxprocs)
	plot_bar_from_counter(disc_proc_counts.most_common(10))
	# plt.xticks(rotation=90)
	plt.title('Discarded top process occurence (10 highest results)')
	if not os.path.exists('plots/!proc'):
		os.mkdir('plots/!proc')
	plt.savefig('plots/!proc/disc_top_process.png')


def plot_rate_xsec(points, cdata='tot_allowed_', folder='', group_name = None):
	# we define a subfunction for plotting A0
	def make_plot(data, tanval, A0val, signvalm, text_short, text_long, limits, cdata, folder, group_names = None):
		# Select what kind of data to plot, 'max' will plot the coverage/xsec of the top process, 'tot_allowed_' will plot what experiments test.
		if cdata == 'max':
			title = 'Top'
		elif cdata == 'disc_max':
			title = 'Discarded top'
		elif cdata == 'tot_allowed_':
			title = 'Total'
		elif cdata == 'tot_disc_':
			title = 'Discarded_total_'
		elif cdata == 'Higgs_mass' or cdata == 'physical_Higgs':
			title = ''
		else:
			print('Wrong cdata argument for plot function, it has to be \"max\" or \"tot_allowed_\"" !')
			exit(1)

		fig, ax = plt.subplots(1)
		cmap = cm.get_cmap('gist_rainbow_r') # Colour map (there are many others)
		# Small differences in plots for xsection and rate
		vmin = 10.**-1
		if text_short == 'rate':
			fig.set_size_inches(8, 5, forward=True)
			if folder == '':
				vmax = 100
			else:
				vmax = max(data['{}{}'.format(cdata, text_short)].tolist())
			norm = colors.Normalize(vmin=0.,vmax=vmax)
			unit = ''
		elif text_short == 'xsec':
			vmax = max(data['{}{}'.format(cdata, text_short)].tolist())
			norm = colors.LogNorm()
			unit='/fb'
		elif text_short == 'higgs':
			text_short = ''
			unit = r'$GeV/c^2$'
			cmap = cm.get_cmap('tab20')
			if text_long == 'physical_Higgs':
				vmin = 0.0
				vmax = 1.0
			else:
				vmax = 129
				vmin = 109
			norm = colors.Normalize(vmin=vmin, vmax=vmax)
		##
		##
		vmin = 0.0
		vmax = max(data['{}{}'.format(cdata, text_short)].tolist())
		norm = colors.Normalize(vmin=vmin, vmax=vmax)
		# Create figures and plots
		ax.xaxis.set_label_text(r'$m_0 [GeV/c^2]$', fontsize=14)
		ax.yaxis.set_label_text(r'$m_{1/2} [GeV/c^2]$', fontsize=14)
		plt.title(r"{title} {text} for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(title=title, sign=signval, tan=tanval, A0=A0val, text=text_long), fontsize=14, loc='left')

		sc = ax.scatter(data['m0'].tolist(), data['mhalf'].tolist(), c=data['{}{}'.format(cdata, text_short)].tolist(), s=190, cmap=cmap,\
		 edgecolor='face', marker='s', alpha=0.75, vmin=vmin, vmax=vmax, norm=norm)

		cb = plt.colorbar(sc, shrink=0.9)
		cb.ax.set_title(text_short+unit, fontsize=10)
		plt.xlim(limits[0], limits[1])
		plt.ylim(0.85*min(data['mhalf'].tolist()), 1.05*max(data['mhalf'].tolist()))

		if '$' in A0val:
			A0val = '-mhalf'

		# drawing exclusion contour
		file = 'DATA/cmssm.txt'
		excl_data = np.loadtxt(file, skiprows=2, usecols = (0,1,2,3,4,5))
		xar = []
		yar = []
		zar = []
		for point in excl_data:
			if point[3] == 0:
				excl_A0 = '0'
			else:
				excl_A0 = '-mhalf'
			if int(point[2]) == int(tanval) and excl_A0==A0val and int(point[4])==int(signval):
				xar.append(int(point[0]))
				yar.append(int(point[1]))
				if point[5] < 1:
					zar.append(0)
				else:
					zar.append(1)
		cont = ax.tricontour(xar, yar, zar, linewidths=2.5, colors='grey', linestyles='--', levels=[0.49,0.5,0.51])


		if folder is not None and folder != '':
			text = folder
		else:
			text = '!'+text_short
		if group_names is not None and len(group_names) > 1:
			text += '_top'

		if not os.path.exists('plots/' + text):
			os.mkdir('plots/' + text)
		# Deal with groups
		group_leg = 'Dominant topology:'
		if group_names is not None:
			group_dict ={}
			for ii, gg in enumerate(sorted(group_names, reverse=True)):
				group_leg += '\n'+ str(ii)+' '+gg
				group_dict[gg] = ii
			# top_g = data['top_group'].to_list()
			# print numbers on points
			for index, row in data.iterrows():
				try:
					if row['maxproc'] is None and row['top_group'] != 'no_data':
						print('[WARNING] Suspicious process:' + row['maxproc'])
					# there might no processes belonging to certain group
					if row['limited_to_group'] == False:
						if row['top_group'] == 'no_data':
							plt.text(row['m0'] - 40, row['mhalf'] - 20, 'X', fontsize=25, fontweight='bold', color='black')
						else:
							if 'disc' in cdata:
								plt.text(row['m0']-45, row['mhalf']-20, group_dict[row['disc_top_group']], fontsize=10)
								# if row['disc_maxrate'] > 5.:
								# 	print('{}_{}_{}_{}_{} : {}'.format(row['m0'], row['mhalf'], row['tanB'], row['A0'], row['sign'], row['disc_maxproc']))
							else:
								plt.text(row['m0']-45, row['mhalf']-20, group_dict[row['top_group']], fontsize=10)


				except KeyError as e:
					print('[WARNING] Point {}_{}_{}_{}_{} has no group set!'.format( row['m0'], row['mhalf'], row['tanB'], row['A0'], row['sign']))

			# print group legend
			if len(group_names) > 1:
				props = dict(boxstyle='round', facecolor='wheat', alpha=0.2)
				plt.gcf().text(0.01, 0.5, group_leg,  fontsize=10, verticalalignment='center', bbox=props)
				fig.subplots_adjust(left=0.3, right=0.99, top=0.85, bottom=0.15)
		else:
			# print on points the value of Higgs mass or the value of total coverage
			# ax.tricontour(data['m0'].tolist(), data['mhalf'].tolist(), data['physical_Higgs'], 1, linewidths=2.5, colors='crimson', linestyles='-')
			if text_short == 'rate' or text_long == 'Higgs_mass' or text_long == 'physical_Higgs':
				if text_short == 'rate':
					fontsize = 10
					toleft = 45
					todown = 20
				else:
					fontsize = 7
					toleft =65
					todown = 10
				for index, row in data.iterrows():
					plt.text(row['m0']-toleft, row['mhalf']-todown, str(int((row['{}{}'.format(cdata, text_short)]))), fontsize=fontsize)


			fig.subplots_adjust(left=0.15, right=0.99, top=0.85, bottom=0.15)

		plt.savefig("plots/{text}/{title}_{stext}_{}_{}_{}.png".format( tanval, A0val, signval, title=title, text=text, stext=text_short))
		plt.close()
################################################################################################################################
	# Select data for plotting
	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'tot_allowed_rate', 'tot_allowed_xsec', 'maxrate', 'maxxsec',\
	          'tot_disc_rate', 'tot_disc_xsec', 'disc_maxrate', 'disc_maxxsec', 'physical_Higgs', 'Higgs_mass',\
	          'disc_maxproc','maxproc', 'disc_top_group', 'top_group', 'limited_to_group' ]
	df = pd.DataFrame.from_records([p.to_dict() for p in points])
	df = df[fields]
	df[fields[:-5]] = df[fields[:-5]].apply(pd.to_numeric)
	
	#df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in points])
	#print(fields[:-5])
	#df[fields[:-5]] = df.loc[:, fields[:-5]].apply(pd.to_numeric)
	
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	# Iterate over four groups (2 vals of tanBeta and signMu)
	plot_higgs = False
	# if not os.path.exists('plots/!higgs'):
	# 	plot_higgs = True
	for gr in groups:
		#gr[fields[:-5]] = gr[fields[:-5]].apply(pd.to_numeric)
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		# Two cases for A0, it's either 0 or -mhalf
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]
		if not zeroA0.empty:
			make_plot(zeroA0, tanval, '0', signval, 'rate', 'coverage', (0, 3150), cdata=cdata, folder=folder, group_names=group_name)
			# make_plot(zeroA0, tanval, '0', signval, 'xsec', 'cross-section', (0, 3150), cdata=cdata, folder=folder)
			if plot_higgs:
				make_plot(zeroA0, tanval, '0', signval, 'higgs', 'Higgs_mass', (0, 3150), cdata='Higgs_mass', folder='!higgs')

		if not nonzeroA0.empty:
			make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'rate', 'coverage', (0, 3150), cdata=cdata, folder=folder, group_names=group_name)
			# make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'xsec', 'cross-section', (0, 3150), cdata=cdata, folder=folder)
			if plot_higgs:
				make_plot(nonzeroA0, tanval, r'$-m_{1/2}$', signval, 'higgs', 'Higgs_mass', (0, 3150), cdata='Higgs_mass', folder='!higgs')
################################################################################################################################


def main(in_path, slha_path, list_of_allowed=None):
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
			xs = 0.0
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
				elif "The total xsec =" in line:# [fb]
					xs = float(line.split()[4])
					# print(xs)
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
			# add infor about total SUSY cross-section
			points[-1].SUSYxsec = xs
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
	print('Analyzing points...')
	for p in points:
		# print('Setting allowed...')
		p.set_allowed(topos, list_of_allowed=list_of_allowed)
		# print('Setting tops...')
		p.set_tops()
		# print('Checking if physical Higgs...')
		p.detect_physical_Higgs()
	print('Analyzing done!')
	return points, broken_files, topos


def groupped_to_file(points, gname):
	processes = [p.allowed_procs for p in points]
	processes = list(itertools.chain.from_iterable(processes))
	names = [p.proc for p in processes]
	unique = sorted(set(names))
	with open('groups/{}'.format(gname+'.txt'), 'w') as f:
		for name in unique:
			f.write(name + '\n')

def get_best_procs(points):
	def get_xs(data):
		SUSYxsec = data['SUSYxsec'].sum()
		allowed = {}
		discarded = {}
		for index, row in data.loc[:,('allowed_procs', 'discarded_procs')].iterrows():
			for p in row['allowed_procs']:
				if p.proc not in allowed:
					allowed[p.proc] = p.xsec
				else:
					allowed[p.proc] += p.xsec
			for p in row['discarded_procs']:
				if p.proc not in allowed:
					discarded[p.proc] = p.xsec
				else:
					discarded[p.proc] += p.xsec
		return SUSYxsec, allowed, discarded

	def to_file(SUSYxsec, allowed, discarded, path, name):
		with open(os.path.join(path, name + '_all.txt'), 'w') as f:
			d = OrderedDict(sorted(allowed.items(),  key=operator.itemgetter(1), reverse=True))
			f.write('process\t\txsec [fb]\trate\n')
			for proc, xs in d.items():
				s = "{}\t{}\t{}%\n".format(proc, xs, round(100.*xs/SUSYxsec, 2))
				f.write(s)
		with open(os.path.join(path, name + '_disc.txt'), 'w') as f:
			d = OrderedDict(sorted(discarded.items(),  key=operator.itemgetter(1), reverse=True))
			f.write('process\t\txsec [fb]\t\txsec/xall\n')
			for proc, xs in d.items():
				s = "{}\t{}\t{}\n".format(proc, xs, round(100.*xs/SUSYxsec, 2))
				f.write(s)

	fields = ['m0', 'mhalf', 'A0', 'tanB', 'sign', 'SUSYxsec', 'allowed_procs', 'discarded_procs']
	df = pd.DataFrame.from_records([p.to_dict() for p in points])
	df = df[fields]
	df[fields[:6]] = df[fields[:6]].apply(pd.to_numeric)
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	results = []
	for gr in groups:
		tanval = gr['tanB'].values[0]
		signval = gr['sign'].values[0]
		# Two cases for A0, it's either 0 or -mhalf
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]
		if not zeroA0.empty:
			SUSYxsec, allowed, discarded = get_xs(zeroA0)
			results.append((SUSYxsec, allowed, discarded))
			to_file(SUSYxsec, allowed, discarded, 'proc_lists/', '{}_{}_{}'.format(tanval, '0', signval))
		if not nonzeroA0.empty:
			SUSYxsec, allowed, discarded = get_xs(nonzeroA0)
			results.append((SUSYxsec, allowed, discarded))
			to_file(SUSYxsec, allowed, discarded, 'proc_lists/', '{}_{}_{}'.format(tanval, '-mhalf', signval))
	# now summarise results for all plains
	totSUSYxsec = 0.0
	totAllowed = {}
	totDiscarded = {}
	for plane in results:
		totSUSYxsec += plane[0]
		for proc, xs in plane[1].items():
			if proc not in totAllowed:
				totAllowed[proc] = xs
			else:
				totAllowed[proc] += xs
		for proc, xs in plane[2].items():
			if proc not in totDiscarded:
				totDiscarded[proc] = xs
			else:
				totDiscarded[proc] += xs
	to_file(totSUSYxsec, totAllowed, totDiscarded, 'proc_lists/', 'total')


def get_proposed(proposed_path):
	proposed = []
	with open(proposed_path, 'r') as file:
		for line in file:
			if len(line.strip()) == 0 or line[0] == '#':
				continue
			else:
				proposed.append(line.strip())
	for ii, proc in enumerate(sorted(set(proposed))):
		print(str(ii+1)+'. '+proc)
	return proposed



if __name__ == '__main__':
	in_path = "DATA/FASTLIM_OUT"
	slha_path = "DATA/SLHA_FIX"
	if len(sys.argv) == 2:
		in_path = str(sys.argv[1])
	elif len(sys.argv) == 3:
		in_path = str(sys.argv[1])
		slha_path = str(sys.argv[1])

	# adding processes that could improve the analyses:
	list_proposed = get_proposed('proposed.txt')

	points, broken_files, topo = main(in_path, slha_path, list_of_allowed=list_proposed)


	print('Detecting groups!')
	groups = []
	for point in points:
		for proc in point.procs:
			if proc.group is not None:
	 			groups.append(proc.group)
	# # groups.append('no_data')
	groups = set(groups)
	print(groups)
	get_best_procs(points)

	#groups = ('G(G->X)', 'G(G->other)')
	print('Plotting basic plots!')
	# plot_rate_xsec(points, group_name=tuple(groups))
	# plot_rate_xsec(points, cdata='tot_disc_', group_name=tuple(groups), folder='!discarded')
	# plot_rate_xsec(points, cdata='disc_max', group_name=tuple(groups), folder='!discarded_max')

	# Now plot the same but instead of top process group plot the total coverage for rate plots
	plot_rate_xsec(points)
	# plot_rate_xsec(points, cdata='tot_disc_', folder='!discarded')
	# plot_hist(points)

	# print('Plotting separate plots for each group')
	#
	# for gg in groups:
	# 	grouped = copy.deepcopy(points)
	#
	# 	for point in grouped:
	# 		point.limit_to_group(gg, topo)
	#
	# 	if len(grouped) > 0:
	# 		print('Dumping processes names')
	# 		groupped_to_file(grouped, gg)
	# 		print('\nPlotting f or {}'.format(gg))
	# 		plot_rate_xsec(grouped, folder=gg.replace('(','').replace(')',''), group_name=(gg,))
	# 		plot_rate_xsec(grouped, cdata='tot_disc_', folder=gg.replace('(', '').replace(')', ''), group_name=(gg,))
	#
	# with open('broken_files.txt', 'w') as bf:
	# 	bf.write('\n'.join(broken_files))




