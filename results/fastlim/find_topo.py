import plot as mplt
from itertools import chain

def proc_eq(p1, p2):
	try:
		if sorted(p1.init_pars) == sorted(p2.init_pars) and sorted(p1.SM_pars) == sorted(p2.SM_pars):
			return True
		else:
			return False
	except Exception as e:
		print(str(e))
		exit(1)

in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
slha_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
points = mplt.main(in_path, slha_path)[0]
procs = list(chain.from_iterable([p.procs for p in points]))
topo = mplt.parse_topo('topologies.txt')

# analyze processes
for p in procs+topo:
	p.analyze_process(None, True)
procs = set(procs)
topo = set(topo)

new_topos = []
topo_names = [p.proc for p in topo]
for pp in procs:
	for tt in topo:
		if proc_eq(pp, tt) and (pp.proc not in topo_names) and ('['+pp.proc+']' not in new_topos):
			if tt.brackets:
				new_topos.append('['+pp.proc+']')
			else:
				new_topos.append(pp.proc)
			continue
new_topos = set(new_topos)


print('New topologies found:')
for nt in new_topos:
	print(nt)


