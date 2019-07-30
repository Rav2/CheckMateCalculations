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
from matplotlib.font_manager import FontProperties
from matplotlib.text import Annotation, Text
from cmssm import Point, Process
from utilities import *


def plot_mass(data):
	signval=1
	tanval=40
	A0val = '-mhalf'
	####
	fig, ax = plt.subplots(1)
	fig.set_size_inches(8, 4, forward=True)
	cmap = cm.get_cmap('tab20')
	vmin = 110.0
	vmax = 130.0
	norm = colors.Normalize(vmin=vmin, vmax=vmax)

	# Create figures and plots
	ax.xaxis.set_label_text(r'$m_0 [GeV/c^2]$', fontsize=14)
	ax.yaxis.set_label_text(r'$m_{1/2} [GeV/c^2]$', fontsize=14)
	plt.title(r"Higgs mass for $\tan(\beta)$={tan}, $sgn$={sign}, $A_0$={A0}".format(sign=signval,\
	                                                                                tan=tanval, A0=A0val), fontsize=14,
	          loc='left')

	sc = ax.scatter(data['m0'].tolist(), data['mhalf'].tolist(), c=data['mass'].tolist(),
	                s=200, cmap=cmap, \
	                edgecolor='face', marker='s', alpha=0.75, vmin=vmin, vmax=vmax, norm=norm)

	cb = plt.colorbar(sc, shrink=0.9)
	cb.ax.set_title('mass [GeV/c^2]', fontsize=10)
	plt.xlim(0, 9500)
	plt.ylim(0, 3500)

	fontsize = 8
	toleft = 125
	todown = 20
	for index, row in data.iterrows():
		plt.text(int(row['m0']) - toleft, int(row['mhalf']) - todown, int(row['mass']), fontsize=fontsize)

	plt.show()


if __name__ == '__main__':
	slha_folder = 'higgs/data/slha_soft/'
	prefix = 'cmssm'
	files = []
	params = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(slha_folder):
		for file in f:
			if file[:5] != prefix:
				continue
			files.append(os.path.join(r, file))
			params.append(file.split('_')[1:3])


	masses = []
	for file in files:
		try:
			masses.append(read_masses(file)['h'])
		except Exception as e:
			masses.append(0.0)

	df = pd.DataFrame(params)
	df.columns = ['m0', 'mhalf']
	df['mass'] = [mass if mass is not None else 0.0 for mass in masses]
	# print(df['m0'][40:60])
	df = df.apply(pd.to_numeric)
	plot_mass(df)



