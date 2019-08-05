import numpy as np 
from collections import OrderedDict

path3 = '../3masses/proc_lists/total_all.txt'
path4 = '../4masses/proc_lists/total_all.txt'

data3 = np.loadtxt(path3, dtype=str, skiprows=1)
data4 = np.loadtxt(path4, dtype=str, skiprows=1)

data3name = data3.transpose()[0]
data4name = data4.transpose()[0]
data4rate = data4.transpose()[2]

data4rate = np.array([float(s[:-1]) for s in data4rate])

new =  np.setdiff1d(data4name, data3name)
d = dict(zip(data4name, data4rate))
d = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))

print('Processes that are allowed for 4 masses but not for 3')
for proc in d:
	if proc in new:
		print('{} : {}%'.format(proc, d[proc]))