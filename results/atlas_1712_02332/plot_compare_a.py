#!/usr/bin/env python

import sys, os, math
from math import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from scipy.interpolate import interp1d

ananame = 'atlas_1712_02332'
sms_topo = r'$pp  \to \tilde q+\tilde q \to q \tilde \chi^0_1 + q \tilde \chi^0_1 $'
#sms_topo = r'$\tilde \chi ^{\pm}_1 \to ??$'

plot_name = '1712_02332_a.pdf'
infile = 'collective_results_QqN1.txt'
atlas_curve = '1712_02332_a.txt'
atlas_up_limit = '1712_02332_a_up.txt'
atlas_down_limit = '1712_02332_a_down.txt'
# load data
data = np.loadtxt(infile, skiprows=2)
xar, yar, zar = data.transpose()
# name, xar, yar, zar, zp, zn = data.transpose()

# kinematical constraint
cond = np.where( xar > yar )
xar = xar[cond]        
yar = yar[cond]        
zar = zar[cond]
# zp = zp[cond]
# zn = zn[cond]

###################################################################################
###################################################################################
###################################################################################
###################################################################################

# declare plot
fig = plt.figure()
ax = fig.add_subplot(111) 

# plot size
fig.subplots_adjust(bottom=0.15, right=0.97, top=0.95, left=0.15)
# axes labels
#ax.set_xlabel(r'$m_{\tilde g} [\rm GeV]$', fontsize=23)
#ax.set_ylabel(r'$m_{\tilde \chi_1^0} [\rm GeV]$', fontsize=23)
ax.set_xlabel(r'$m_{\tilde q} [\rm GeV]$', fontsize=23)
ax.set_ylabel(r'$m_{\tilde \chi_1^0} [\rm GeV]$', fontsize=23)
# axes ranges
ax.set_xlim([min(xar)*0.5, max(xar)*1.05])
ax.set_ylim([min(yar)*0.9, max(yar)*1.25])

# ticks font
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14) 

 
obs0 = np.loadtxt(atlas_curve, delimiter='\t').transpose()
obsup = np.loadtxt(atlas_up_limit, delimiter='\t').transpose()
obsdw = np.loadtxt(atlas_down_limit, delimiter='\t').transpose()

lw_exp_0 = 2.5
lw_exp_er = 2.
op = 1.
c_exp = 'dodgerblue'

ax.plot(obs0[0], obs0[1], lw=lw_exp_0, ls='-', c=c_exp, alpha=op)
ax.plot(obsup[0], obsup[1], lw=lw_exp_er, ls='--', c=c_exp, alpha=op)
ax.plot(obsdw[0], obsdw[1], lw=lw_exp_er, ls='--', c=c_exp, alpha=op)



# scatter plot
vmin, vmax = 10**-2, 10
sc = ax.scatter(xar, yar, s=20, c=zar, cmap='nipy_spectral', norm=cls.LogNorm(), 
	vmin=vmin, vmax=vmax, lw=0.5, edgecolors='none', marker='s', alpha=0.7, rasterized=False)    
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
# ax.tricontour(xar,yar,zp,  levels, linewidths=lw_er, colors='r', linestyles='--')
# ax.tricontour(xar,yar,zn,  levels, linewidths=lw_er, colors='r', linestyles='--')

# diagonal lines
#ax.plot([0,3000],[0,3000],lw=1,c='gray')
#ax.fill_between([0,3000], [0,3000], [3000,3000], lw=1, hatch='xxx', facecolor='', edgecolor="k")
ax.fill_between([0,3000], [0,3000], [3000,3000], lw=1, alpha=0.3, facecolor='gray')
#ax.fill_between([0,3000], 200, 300)

# legend
xwid = (max(xar) - min(xar))
ywid = (max(yar) - min(yar))
x0 = min(xar) - 0.15*xwid
y0 = min(yar) + 1.15*ywid
ax.text(x0, y0, ananame, fontsize=10)
y1 = y0 - 0.08*ywid
ax.text(x0, y1, sms_topo, fontsize=10)
y2 = y1 - 0.08*ywid
x1 = x0 + 0.1*xwid
ax.plot([x0,x1],[y2,y2],lw=lw_exp_0-0.5,c=c_check)
dy = 0.02*ywid
# ax.plot([x0,x1],[y2+dy,y2+dy],lw=lw_exp_er-0.5,ls='--',c=c_check)
# ax.plot([x0,x1],[y2-dy,y2-dy],lw=lw_exp_er-0.5,ls='--',c=c_check)
x2 = x1 + 0.03*xwid
ax.text(x2, y2*0.99, 'CheckMATE', fontsize=10)

y2 = y2 - 0.09*ywid
ax.plot([x0,x1],[y2,y2],lw=lw_exp_0,c=c_exp)
dy = 0.02*ywid
ax.plot([x0,x1],[y2+dy,y2+dy],lw=lw_exp_er,ls='--',c=c_exp)
ax.plot([x0,x1],[y2-dy,y2-dy],lw=lw_exp_er,ls='--',c=c_exp)
x2 = x1 + 0.03*xwid
ax.text(x2, y2*0.94, 'ATLAS\nw. theo-err', fontsize=10)

# ##########################################

tag = infile.split('.')[0]
fig.savefig(plot_name)
print plot_name
plt.show()

#exit()
