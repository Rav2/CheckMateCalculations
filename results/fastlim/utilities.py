#import xslha

import pyslha
from cmssm import Process
import copy

def parse_topo(topo_file):
	processes = []
	with open(topo_file, 'r') as file:
		data = file.readlines()
		for line in data:
			if len(line) > 0 and line[0] == '#':
				continue
			else:
				for proc in line.strip().split():
					if proc[0] == '(':
						if proc[-1] == ')':
							processes.append(Process(proc[1:-1], 0., 0., False))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append(Process(proc[1:], 0., 0., False))
					elif proc[-1] == ')':
						print('[WARNING] {} without starting bracket! Will try to parse anyway.'.format(proc))
						processes.append(Process(proc[:-1], 0., 0., False))
					elif proc[0] == '[':
						if proc[-1] == ']':
							processes.append(Process(proc[1:-1], 0., 0., True))
						else:
							print('[WARNING] {} without ending bracket! Will try to parse anyway.'.format(proc))
							processes.append(Process(proc[1:], 0., 0., True))
					elif proc[-1] == ']':
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
		return 'w'
	elif ppid in (12,14,16):
		return 'n'
	elif ppid == 23:
		return 'z'
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
	d = pyslha.read(slha_path)
	mb = d.blocks['MASS']
	masses = {}
	for par in mb.items():
		name = get_name(int(par[0]))
		if name is not None:
			masses[name] = abs(par[1])
	# add some SM masses by hand
	masses['z'] = 91.1876
	masses['n'] = 0.120 * 10**-9
	masses['q'] = 1./4.*(2.3+4.8+1275+95)*10**-3
	masses['e'] = 0.5109989461 * 10**-3
	masses['m'] = 105.6583745 * 10**-3
	# now deal with R,L chiralities
	new_masses = {}
	for par in masses.items():
		name = str(par[0])
		if name[-1] == 'R' or name[-1] == 'L':
			m = 0.5 * (masses[name[:-1] + 'R'] + masses[name[:-1] + 'L'])
			if name[0] != 'N':
				assert m > 0, 'Mass of {} should be >0'.format(name)
			new_masses[name[:-1]] = abs(m)
	new_masses['Q'] = 1. / 4. * (new_masses['U'] + new_masses['D'] + new_masses['S'] + new_masses['C'])
	return {**masses, **new_masses}
