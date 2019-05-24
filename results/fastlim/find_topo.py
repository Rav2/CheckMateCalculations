import plot as mplt
from itertools import chain

def get_proc_inits(proc):
	par1 = proc.split('_')[0]
	par2 = proc.split('_')[1]
	names = []
	for p in (par1, par2):
		if p[0] in ('G', 'Q', 'E'):
			names.append(p[0])
		elif p[0:2] in ('N1', 'N2', 'N3', 'N4', 'T1', 'T2', 'B1', 'B2', 'C1', 'C2'):
			names.append(p[0:2])
		elif p[0:3] == 'TAU':
			names.append(p[0:4])
	assert len(names)==2, 'There must be 2 names!'
	names.sort()
	return names

def get_SM_products(proc):
	par1 = proc.split('_')[0]
	par2 = proc.split('_')[1]
	prods = []
	for p in (par1, par2):
		for ii,char in enumerate(p):
			if char in ('q', 'e', 'b', 't', 'g', 'z', 'h', 'w', 'n', 'm'):
				if char=='t' and len(p)>ii+1 and p[ii+1]=='a':
					prods.append('ta')
				else:
					prods.append(char)
	prods.sort()
	return prods

in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
slha_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
points = mplt.main(in_path, slha_path)[0]
procs = set(list(chain.from_iterable([p.procs for p in points])))
topo = mplt.parse_topo('topologies.txt')
topo_procs = [p[0] for p in topo]

topo_tuples = []
for tup in topo:
	proc = tup[0]
	names = get_proc_inits(proc)
	sm_prods = get_SM_products(proc)
	topo_tuples.append((names, sm_prods))


new_topos = []
for proc in procs:
	names = get_proc_inits(proc)
	sm_prods = get_SM_products(proc)
	if names is not None and sm_prods is not None:
		proc_tuple = (names, sm_prods)
		if proc_tuple in topo_tuples and proc not in topo_procs:
			new_topos.append(proc)
			# print(proc, proc_tuple)
			print(proc)

