import numpy as np
import pandas as pd
import csv
from collections import OrderedDict

path = 'proc_lists/'
infiles = [ '5_-mhalf_-1_all.txt', '5_-mhalf_1_all.txt',\
 '5_0_-1_all.txt', '5_0_1_all.txt', '40_-mhalf_-1_all.txt',\
  '40_-mhalf_1_all.txt', '40_0_-1_all.txt', '40_0_1_all.txt']

dicts = []

rows = np.loadtxt(path+'total_all.txt', dtype=str, skiprows=1, usecols=(0,2))
cols = rows.transpose()
rates = []
topos = []
for topo in cols[0]:
	topos.append(topo.replace('_', '\\_'))
for rate in cols[1]:
	rates.append(rate.replace('%', '\%'))
new_cols = (topos, rates)
df = pd.DataFrame({'Topology' : new_cols[0],'Total' : new_cols[1]})



for file in infiles:
	rows = np.loadtxt(path+file, dtype=str, skiprows=1, usecols=(0,2))
	cols = rows.transpose()
	rates = []
	topos = []
	for topo in cols[0]:
		topos.append(topo.replace('_', '\\_'))
	for rate in cols[1]:
		rates.append(rate.replace('%', '\%'))
	new_cols = (topos, rates)

	plane_name = file.split('.')[0].split('_')
	name = ('('+plane_name[0]+','+plane_name[1]+','+plane_name[2]+')').replace('-mhalf', r'$-m_{1/2}$')
	cdf = pd.DataFrame({'Topology' : new_cols[0], name : new_cols[1]})
	df = pd.merge(left=df,right=cdf, how='left', left_on='Topology', right_on='Topology', validate='one_to_one')
df.index += 1
df = df.fillna('0.0\%')

# print(df)
df.to_csv('table.txt', sep = '&', line_terminator='\\\\\n', quotechar=' ')#quoting=csv.QUOTE_NONE)


