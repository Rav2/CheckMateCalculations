#!/usr/bin/env python
#
# This script combines cmssm and UML results
#

import os
import sys
import plotCMSSM as pMS
import plotUML as pUML
import scipy as scp
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import neighbors, svm
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix
from matplotlib.colors import ListedColormap
import matplotlib.colors as cls
from mpl_toolkits.mplot3d import Axes3D
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.lines as mlines
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from scipy.interpolate import *
from sklearn.svm import SVR, SVC
from scipy.interpolate import interpn, RegularGridInterpolator
from scipy.optimize import curve_fit
import pyslha
import math as m
from scipy.stats import norm
import matplotlib.mlab as mlab
from matplotlib.patches import Patch

def readUML(infile):
	"""
	Read UML data from file.
	:param infile: File containing UML data.
	:return: UML data as numpy array.
	"""
	plot_prefix = 'minigrid'
	# load data
	data = np.loadtxt(infile, skiprows=2, usecols=range(0,5))
	return data


def readCMSSM(infile):
	"""
	Read cMSSM 5D data from input file.
	:param infile: Input file.
	:return: Data as numpy array.
	"""
	plot_prefix = 'cmssm'
	# load data
	data = np.loadtxt(infile, skiprows=2, usecols=range(0,6))
	return data

def gauss(x, mu, sigma):
	def func(p, mean, stdev):
		return 1.0/m.sqrt(2*m.pi * stdev**2) * m.e **((-1*(p-mean)**2)/(2*stdev**2))
	X = np.array(x)
	if X.size == 1:
		print('Single value')
		return func(X, mu, sigma)
	else:
		result = []
		for p in X:
			result.append(func(p, mu, sigma))
		return result



def cMSSMtoUML(cmssm_data, slha_folder):
	"""
	Takes points in 5D parameter space of cMSSM, reads appropriate SLHA files, and finds the corresponding four parameters of UML.
	:param cmssm_data: Numpy array with cMSSM parameter values.
	:param slha_folder: Relative path to folder where cMSSM SLHA files are stored.
	:return: Return numpy array (N,4)
	"""

	translated_data = []
	for pp in cmssm_data:
		name = "cmssm_{}_{}_{}_{}_{}.slha".format(int(pp[0]), int(pp[1]), int(pp[2]), int(pp[3]), int(pp[4]))
		try:
			with open(os.path.join(slha_folder, name), 'r') as file:
				d = pyslha.read(file.name)
				mG = d.decays[1000021].__dict__['mass']
				QL = [d.decays[1000000 + ii].__dict__['mass'] for ii in (1,2,3,4)]
				QR = [d.decays[2000000 + ii].__dict__['mass'] for ii in (1,2,3,4)]
				mQ = 1./8. * (sum(QL)+sum(QR))
				Q3L = [d.decays[1000000 + ii].__dict__['mass'] for ii in (5,6)]
				Q3R = [d.decays[2000000 + ii].__dict__['mass'] for ii in (5,6)]
				mQ3 = 1./4. * (sum(Q3L)+sum(Q3R))
				mN1 = d.decays[1000022].__dict__['mass']
				translated_data.append((mG, mQ, mQ3, mN1))
		except FileNotFoundError:
			print(os.path.join(slha_folder, name) + ' NOT FOUND!')
	translated_data = np.array(translated_data)
	# print(np.array(cmssm_data).shape, translated_data.shape)
	return translated_data


def plotUML(data, mGval, markersize=50):
	"""
	Calls for external function plotting UML data as 3D projections with constant mG.
	:param data: Numpy array with UML points and r values (N, 4)
	:param mGval: The value of mG for the projection.
	:param markersize: Size of the UML points.
	:return: Return a figure object with the plot.
	"""
	labelsG = [r'$m_Q$', r'$m_{Q_3}$', r'$m_{\chi^0_1}$', r'$m_G$']
	labels2G = ['Q', 'Q3', 'N1', 'G']
	labelsN = [r'$m_Q$', r'$m_{Q_3}$', r'$m_G$', r'$m_{\chi^0_1}$']
	labels2N = ['Q', 'Q3', 'G', 'N1']

	# plot with mG slices
	return pUML.do_plot(data['mQ'].values, data['mQ3'].values, data['mN1'].values, mGval, data['r'].values, labelsG, 'G', save=False, markersize=markersize)


def getRGmap():
	"""
	Creates a red to green color map to visualize r exclusion parameter.
	:return: Colormap object.
	"""
	# Recreate UML color map
	colors1 = plt.cm.hot(np.linspace(0.5, 0.1, 128))
	colors2 = plt.cm.summer(np.linspace(0.0, 0.5, 128))
	colors = np.vstack((colors2, colors1))
	mymap = cls.LinearSegmentedColormap.from_list('my_colormap', colors)
	return mymap

def transform_r(r):
	return r
	# maxr = float(max(r))
	# return [val if val < 1 else 1. + val/maxr for val in r]
	# return np.log([10**-5 if val < 10**-5 else val for val in r])
	return [val if val < 40 else 40 for val in r]
def untransform_r(r, maxr):
	return r
	# return [val if val < 1 else  ((val - 1.)*maxr) for val in r]
	# return np.exp(r)


def model_fit(data, visualize=False):
	"""
	Train Machine Learning model on UML data and optionally visualize.
	:param data: UML data, (N, 5).
	:param visualize: If True, plots will be shown, presenting the effect of fitting the model against dense meshgrid.
	:return: Sklearn model fitted to UML data.
	"""
	df = pd.DataFrame(data)
	df.columns = ['mG', 'mQ', 'mQ3', 'mN1', 'r']
	# df['excluded'] = np.where(df['r'] < 1, 0, 1)
	# print(df.head(20))
	# We take masses as the data and excluded as the classifier
	X = df.loc[:, ('mG', 'mQ', 'mQ3', 'mN1')]
	y = df['r']

	scaler = None
	# scaler = RobustScaler().fit(X.values)
	rescaled_X =  np.array(X)
	# rescaled_X = scaler.transform(X.values)
	max_y = max(y)
	print('Max original y={}'.format(max_y))
	rescaled_y = transform_r(y) #[val if val < 1. else 1.+val/max_y for val in y]
	y_sum = sum(rescaled_y)
	print('Sum rescaled y={}'.format(y_sum))
	rescaled_y = np.array(rescaled_y)

	quantised = [0 if val < 1 else 1 for val in y]
	print('Mean class = {}'.format(np.mean(quantised)))
	print('Excluded = {}, allowed = {}'.format(sum(quantised), len(quantised)-sum(quantised)))
	# plt.hist(y, 50, range=(0, 5))
	# plt.show()
	# exit(1)
	# model = LinearNDInterpolator(rescaled_X, rescaled_y, fill_value=1-10**-10)#, rescale = True)
	model = NearestNDInterpolator(rescaled_X, rescaled_y, rescale=True)
	# model = RandomForestRegressor(n_estimators=300, max_depth=15)
	# model = RandomForestRegressor(n_estimators=50, warm_start=True)
	# model = GradientBoostingRegressor(loss='ls')
	# model = GradientBoostingRegressor(loss='lad', n_estimators=50, warm_start=True)
	# model = SVR(kernel='rbf', gamma='scale', C=1)#, C = 10., epsilon=0.01)
	# model = KNeighborsRegressor(10, weights='uniform')

	# xx = np.linspace(0, 2,len(y)).tolist()
	# weights = np.array(gauss(xx, 1, 0.5))
	# model.fit(rescaled_X, rescaled_y)#, sample_weight=weights)

	# scores = []
	# cv = KFold(n_splits=12, shuffle=False)
	# for train_index, test_index in cv.split(rescaled_X):
	# 	X_train, X_test, y_train, y_test = rescaled_X[train_index], rescaled_X[test_index], rescaled_y[train_index], rescaled_y[test_index]
	# 	# weigths_train = weights[train_index]
	# 	model.fit(X_train, y_train)#, sample_weight=weigths_train)
	# 	# model.n_estimators += 100
	# 	scores.append(model.score(X_test, y_test))
	# 	print('Model score = {}'.format(model.score(X_test, y_test)))
	# 	Z = [0. if val < 1 else 1 for val in untransform_r(model(X_test), max_y)]
	# 	Y = [0. if val < 1 else 1 for val in y_test]
	# 	# print("Mean r for refitting check is {}".format(np.mean(Z)))
	# 	cm = confusion_matrix(Y, Z)
	# 	list1 = ["Actual 0", "Actual 1"]
	# 	list2 = ["Predicted 0", "Predicted 1"]
	# 	print(pd.DataFrame(cm, list1, list2))
	# print('Mean score')
	# print(np.mean(scores))

	# model =  NearestNDInterpolator(X, Y, rescale=False)
	if visualize:
		groups = df.groupby('mG')
		group_names = df['mG'].unique()
		for mGval in group_names:
			cg = groups.get_group(mGval)

			# Create a meshgrid which will be used to visualize areas for different classes
			mQ_min, mQ_max = cg['mQ'].min() - 1, cg['mQ'].max() + 1
			mQ3_min, mQ3_max = cg['mQ3'].min() - 1, cg['mQ3'].max() + 1
			mN1_min, mN1_max = cg['mN1'].min() - 1, cg['mN1'].max() + 1
			q, q3, n1 = np.meshgrid(np.arange(mQ_min, mQ_max, (mQ_max-mQ_min)/15.), np.arange(mQ3_min, mQ3_max, (mQ3_max-mQ3_min)/15.),\
			 np.arange(mN1_min, mN1_max, (mN1_max-mN1_min)/15.))
			rav = np.c_[[mGval for x in q.ravel()], q.ravel(), q3.ravel(), n1.ravel()]
			if scaler is not None:
				rav_trans = scaler.transform(rav)
			else:
				rav_trans = rav
			Z = untransform_r(model(rav_trans), max_y)
			# Z = [val+1 for val in Z]
			# Z = [val if val<1 else (val - 1)*max_y for val in Z]
			# Z = np.array([val if val<1 else (val-1)*max_y for val in Z])
			print("Mean predicted r for mG={m} is {a1}, mean r for mG={m} is {a2}".format(m=mGval, a1=round(np.mean(Z),5), a2=round(np.mean(cg['r'].tolist()), 5)))
			# Plot data points for UML
			# fig = plotUML(cg, mGval, markersize = 15)
			# ax = fig.get_axes()[0]
			
			# Plot meshgrid points
			# ax.scatter(rav[:,1], rav[:,2], rav[:,3], c=Z, s=150, edgecolors='none', marker='s', cmap=getRGmap(), alpha=0.05)
			# plt.show()

	return model, scaler, max_y

def plot_raw_distr(r, save=False):
	n, bins, patches = plt.hist(r, color='blue')
	plt.title('distribution of r')
	plt.text(0.0, 0.9 * max(n), r'$\mean={}$'.format(round(np.mean(r), 3)))
	if save:
		plt.savefig('plots/r_distr.png')
	else:
		plt.show()



def plotCMSSM(data, isZeroA0):
	"""
	Create a cMSSM plot with r exclusion parameter distribution and an excludion contour.
	:param data: cMSSM data, (N, 6)
	:param isZeroA0: Set True for A0=0, False for A0=-m1/2. Used for labels.
	:return: Returns a figure with cMSSM plot.
	"""
	labels = (r'$m_0$', r'$m_{1/2}$', r'$tan \beta$', r'$A_0$', r'$sgn(\mu)$')
	# plot m0 vs mhalf
	return pMS.do_plot(data, labels, isZeroA0)

def plotHist(cMSSMdata, model, scaler, maxr, slha_folder, save=False):
	df = pd.DataFrame(cMSSMdata)
	df.columns = ['m0', 'mhalf', 'tanB', 'A0', 'sign', 'r']
	data = df.loc[:,('m0', 'mhalf', 'tanB', 'A0', 'sign')].values
	rCMSSM = df['r'].tolist()
	translData = cMSSMtoUML(data, slha_folder)
	if scaler is not None:
		translData = scaler.transform(translData)

	rPredicted = untransform_r(model(translData), maxr)
	# rPredicted = [val if val<1 else (val-1)*max(rCMSSM) for val in rPredicted]
	assert len(rCMSSM) == len(rPredicted)
	diff = []
	for ii in range(0, len(rCMSSM)):
		diff.append(rCMSSM[ii]-rPredicted[ii])
	# print(diff)
	fig, ax = plt.subplots()
	color='green'

	mean = np.mean(diff)
	variance = np.var(diff)
	sigma = np.sqrt(variance)
	print('Hist parameters: mean={}, sigma={}'.format(mean, sigma))

	n, bins, patches = ax.hist(diff, 11, density=True, range=(mean-2*sigma, mean+2*sigma), color=color)
	limit = max
	x = np.linspace(mean-3*sigma, mean+3*sigma, 100)
	fit, = ax.plot(x, mlab.normpdf(x, mean, sigma), color='orange')
	plt.legend((Patch(color=color), fit), ('data', 'fit'))
	plt.xlim((mean-3*sigma, mean+3*sigma))
	plt.xlabel(r'$r_{cMSSM}-r_{pred}$')
	plt.ylabel('Probability distribution')
	plt.title('Distribution of the difference between true and predicted r')
	plt.text(mean-2.8*sigma, 0.9*max(n), r'$\mu={}$'.format(round(mean,3))+'\n'+r'$\sigma={}$'.format(round(sigma,3)))

	if save:
		plt.savefig('plots/hist.png')
	else:
		plt.show()

	plt.clf()
	plt.close()
	return mean, sigma

def plotR(cMSSMdata, model, scaler, maxr, slha_folder, save=False, sigma=0):
	df = pd.DataFrame(cMSSMdata)
	df.columns = ['m0', 'mhalf', 'tanB', 'A0', 'sign', 'r']
	data = df.loc[:, ('m0', 'mhalf', 'tanB', 'A0', 'sign')].values
	rCMSSM = df['r'].tolist()
	translData = cMSSMtoUML(data, slha_folder)
	if scaler is not None:
		translData = scaler.transform(translData)
	rPredicted = untransform_r(model(translData), maxr)
	# rPredicted = [val if val < 1 else (val - 1) * max(rCMSSM) for val in rPredicted]

	both_allowed_cmssm = []
	both_allowed_pred = []
	both_excluded_cmssm = []
	both_excluded_pred = []
	mixed_cmssm = []
	mixed_pred = []
	for ii, val in enumerate(rCMSSM):
		if val < 1 and rPredicted[ii] < 1:
			both_allowed_cmssm.append(val)
			both_allowed_pred.append(rPredicted[ii])
		elif val >= 1 and rPredicted[ii] >= 1:
			both_excluded_cmssm.append(val)
			both_excluded_pred.append(rPredicted[ii])
		else:
			mixed_cmssm.append(val)
			mixed_pred.append(rPredicted[ii])

	fig, ax = plt.subplots()
	maxr = max((max(rPredicted), max(rCMSSM)))
	minr = min(min(rPredicted), min(rCMSSM))
	xx = np.linspace(10**-20, maxr*3, 20000)
	plt.xlim(10**-1, maxr *3)
	plt.ylim(10**-1, maxr *3)
	ax.plot(xx, xx, linestyle='--', color='black')

	if sigma > 0:
		yyUp = [val + m.sqrt(2)*sigma for val in xx]
		yyDown = [val - m.sqrt(2) * sigma for val in xx]
		yyUp2 = [val + 2*m.sqrt(2) * sigma for val in xx]
		yyDown2 = [val - 2*m.sqrt(2) * sigma for val in xx]
		ax.plot(xx, yyUp, linestyle='dashdot', color='black')
		ax.plot(xx, yyDown, linestyle='dashdot', color='black')
		ax.plot(xx, yyUp2, linestyle='dotted', color='black')
		ax.plot(xx, yyDown2, linestyle='dotted', color='black')
		ax.fill_between(xx, yyUp, yyDown, color='blue', alpha=0.25)
		ax.fill_between(xx, yyUp2, yyDown2, color='blue', alpha=0.15)

	sc1 = ax.scatter(both_excluded_cmssm, both_excluded_pred, marker='s', c='red', alpha=0.85, edgecolors='black', linewidths='1')
	sc2 = ax.scatter(mixed_cmssm, mixed_pred, marker='^', c='yellow', alpha=0.85, edgecolors='black', linewidths='1')
	sc3 = ax.scatter(both_allowed_cmssm, both_allowed_pred, marker='o', c='green', alpha=0.85, edgecolors='black', linewidths='1')

	def f(x, A, B): # this is your 'straight line' y=f(x)
		return A*x + B
	
	nrCMSSM = np.log10([r+10**-20 if r == 0 else r for r in rCMSSM])
	nrPredicted = np.log10([r+10**-20 if r == 0 else r for r in rPredicted])
	coefficients, pcov = curve_fit(f, nrCMSSM, nrPredicted) # your data x, y to fit
	# coefficients = np.polyfit(nrCMSSM, nrPredicted, 1)
	a = coefficients[0]
	b= coefficients[1]
	yfit = np.array([10**(a*np.log10(x) + b) for x in xx])
	fit = ax.plot(xx, yfit, linestyle='-', color='orange')
	print('Fitting least squares: a={}, b={}'.format(coefficients[0], coefficients[1]))

	fit_line = mlines.Line2D([], [], color='orange', label='fit')
	plt.legend((sc1, sc2, sc3, fit_line), ('both excluded', 'mixed', 'both allowed', 'fit log(y)=alog(x)+b'))
	ax.set_xscale('log', basex=10)
	ax.set_yscale('log', basey=10)
	plt.title('r exclusion parameter; cMSSM vs UML prediction')
	plt.xlabel('cMSSM')

	plt.ylabel('UML prediction')
	if save:
		plt.savefig('plots/cMSSM_vs_UML.png')
	else:
		plt.show()
	plt.clf()
	plt.close()


def combine(cMSSMdata, model, scaler, maxr, slha_folder, save=False):
	"""
	Creates a cMSSM plot, uses the data to obtain a grid in UML parameter space, fits these points against trained model,
	draws a second contour based on UML classification.
	:param cMSSMdata: Data in cMSSM parameter space, numpy array (N, 6)
	:param model: Previously trained model on UML grid.
	:param slha_folder: Path to folder containing SLHA files for cMSSM points.
	:param save: If True, plots will be saved on disk. If False, they will be shown on screen.
	:return: -
	"""
	df=pd.DataFrame(cMSSMdata)
	df.columns = ['m0', 'mhalf', 'tanB', 'A0', 'sign', 'r']
	gb = df.groupby(['tanB', 'sign'], sort=True)
	groups = [gb.get_group(x) for x in gb.groups]
	sigma = 5.0
	# Iterate over four groups (2 vals of tanBeta and signMu)
	for gr in groups:
		gr = gr.apply(pd.to_numeric)
		# Two cases for A0, it's either 0 or -mhalf
		zeroA0 = gr[gr['A0'] == 0]
		nonzeroA0 = gr[gr['A0'] != 0]

		# extract projection type
		tanval = str(int(gr['tanB'].values[0]))
		sign = str(int(gr['sign'].values[0]))

		# drawing options for new contour
		lw_0 = 2.5
		lw_er = 1.5
		c_check = 'magenta'
		blue_line = mlines.Line2D([], [], color='blue', label='cMSSM excl. cont.')
		mag_line = mlines.Line2D([], [], color='magenta', label='UML excl. cont.')
		handles = (blue_line, mag_line)
		levels = [0.49,0.5,0.51]
		if not zeroA0.empty:
			fig = plotCMSSM(zeroA0, True)
			ax = fig.get_axes()[0]
			translData = cMSSMtoUML(zeroA0.values, slha_folder)
			if scaler is not None:
				translData = scaler.transform(translData)
			z = untransform_r(model(translData), maxr)
			# z = [val if val <1 else (val-1)*max(df['r'].tolist()) for val in model(translData)]
			z_norm = [0 if val<1 else 1 for val in z]
			print('--- INFO ABOUT UML SCAN ---')
			print('tanB={}, A0={}, sgn={}'.format(tanval, '0', sign))
			print(
				'allowed={}, excluded={}, total={}, excl. fraction={}'.format(len(z_norm) - sum(z_norm), sum(z_norm),
				                                                              len(z_norm), \
				                                                              float(sum(z_norm)) / float(
					                                                              len(z_norm))))
			# Uncomment to plot r for translated values
			# sc = ax.scatter(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), s=130, c=z, cmap=getRGmap(), norm=cls.LogNorm(), \
			# 	vmin=10**-2, vmax=10**2, lw=0.5, edgecolors='none', marker='s', alpha=0.7, rasterized=False)
			# cb = plt.colorbar(sc)
			ax.tricontour(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), z_norm, linewidths=lw_0, colors=c_check, linestyles='-', levels=levels)
			z_more = [0 if (val + sigma) < 1 else 1 for val in z]
			z_less = [0 if (val - sigma) < 1 else 1 for val in z]
			# ax.tricontour(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), z_less, linewidths=lw_0, colors=c_check, linestyles='dotted', levels=levels)
			# ax.tricontour(zeroA0['m0'].tolist(), zeroA0['mhalf'].tolist(), z_more, linewidths=lw_0, colors=c_check, linestyles='dotted', levels=levels)
			legend = ax.legend(handles=handles, bbox_to_anchor=(-0.29, -0.21, 0.5, 0.5))
			if save:
				plt.savefig('plots/{}_{}_{}.png'.format(tanval, '0', sign))
			else:
				plt.show()
		if not nonzeroA0.empty:
			fig = plotCMSSM(nonzeroA0, False)
			ax = fig.get_axes()[0]
			translData = cMSSMtoUML(nonzeroA0.values, slha_folder)
			if scaler is not None:
				translData = scaler.transform(translData)
			z = untransform_r(model(translData), maxr)
			# z = [val if val < 1 else (val - 1) * max(df['r'].tolist()) for val in model(translData)]
			z_norm = [0 if val < 1 else 1 for val in z]
			print('--- INFO ABOUT UML SCAN ---')
			print('tanB={}, A0={}, sgn={}'.format(tanval, '-mhalf', sign))
			print(
				'allowed={}, excluded={}, total={}, excl. fraction={}'.format(len(z_norm) - sum(z_norm), sum(z_norm),
				                                                              len(z_norm), \
				                                                              float(sum(z_norm)) / float(
					                                                              len(z_norm))))
			# Uncomment to plot r for translated values
			# sc = ax.scatter(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), s=130, c=z, cmap=getRGmap(), norm=cls.LogNorm(), \
			# 	vmin=10**-2, vmax=10**2, lw=0.5, edgecolors='none', marker='s', alpha=0.7, rasterized=False)
			# cb = plt.colorbar(sc)
			ax.tricontour(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), z_norm, linewidths=lw_0, colors=c_check, linestyles='-', levels=levels)
			z_more = [0 if (val + sigma) < 1 else 1 for val in z]
			z_less = [0 if (val - sigma) < 1 else 1 for val in z]
			# ax.tricontour(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), z_less, linewidths=lw_0, colors=c_check, linestyles='dotted', levels=levels)
			# ax.tricontour(nonzeroA0['m0'].tolist(), nonzeroA0['mhalf'].tolist(), z_more, linewidths=lw_0, colors=c_check, linestyles='dotted', levels=levels)
			legend = ax.legend(handles=handles, bbox_to_anchor=(-0.29, -0.21, 0.5, 0.5))
			if save:
				plt.savefig('plots/{}_{}_{}.png'.format(tanval, '-mhalf', sign))
			else:
				plt.show()
	plt.clf()
	plt.close()
		
	

if __name__ == "__main__":
	# read UML data
	dataUML = readUML('data/UML.txt')
	# plot UML grid
	# plotUML(dataUML)

	# test_regressors(dataUML)

	# Fit model using UML grid, and eventually show it
	model, scaler, maxr = model_fit(dataUML, visualize=True)

	# Load cMSSM data
	dataCMSSM = readCMSSM('data/cmssm.txt')
	# Combine results and plot

	combine(dataCMSSM, model, scaler, maxr, 'data/SLHA_FIX', save=True)
	mean, sigma = plotHist(dataCMSSM, model, scaler, maxr, 'data/SLHA_FIX', save=True)
	plotR(dataCMSSM, model, scaler, maxr, 'data/SLHA_FIX',  sigma=sigma, save=True)
