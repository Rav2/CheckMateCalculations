import plot as mplt
from itertools import chain
import cmssm

def proc_eq(p1, p2):
	try:
		if sorted(p1.SM_pars) == sorted(p2.SM_pars):
			return True
		else:
			return False
	except Exception as e:
		print(str(e))
		exit(1)

def validate_topo(proc):
	br1 = proc.proc.split('_')[0]
	br2 = proc.proc.split('_')[1]
	# check for LSP
	if len(br1) >=2 and len(br2) >=2 and br1[-2:] == 'N1' and br2[-2:] == 'N1':
		return True
	else:
		print('N1 is not LSP: {}'.format(proc.proc))
		return False

def electron2muon(topos, topo_names):
	new_topos = []
	for topo in topos:
		br1 = topo.proc.split('_')[0]
		br2 = topo.proc.split('_')[1]
		new_br1 = []
		new_br2 = []
		if 'Ee' in br1:
			new_br1.append(br1.replace('Ee', 'Mm'))
		else:
			if 'E' in br1:
				new_br1.append(br1.replace('E', 'M'))
			if 'e' in br1:
				new_br1.append(br1.replace('e', 'm'))
		if 'Ee' in br2:
			new_br2.append(br2.replace('Ee', 'Mm'))
		else:
			if 'E' in br2:
				new_br2.append(br2.replace('E', 'M'))
			if 'e' in br2:
				new_br2.append(br2.replace('e', 'm'))

		for b1 in new_br1:
			for b2 in new_br2:
				if b1<b2:
					s = b1+'_'+b2
				else:
					s = b2 + '_' + b1
				# print(s)
				new_topos.append(s)
	result = []
	for nt in new_topos:
		if nt not in topo_names:
			result.append(nt)
	return result

if __name__ == '__main__':
	in_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/results/fastlim/FASTLIM_OUT"
	slha_path = "/Users/rafalmaselek/Projects/CheckMateCalculations/results/fastlim/SLHA_FIX"
	points = mplt.main(in_path, slha_path)[0]
	procs = list(chain.from_iterable([p.procs for p in points]))
	topo = mplt.parse_topo('topologies.txt')

	# analyze processes to extract particles
	for p in procs+topo:
		p.analyze_process(None, True)
		if not validate_topo(p):
			cmssm.drawFullTree(p.decayTree)
		# print('#'*40)

	procs = list(set(procs))
	topo = set(topo)

	print('Looking for new topologies...')
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
	new_topos += electron2muon(topo, topo_names)
	new_topos = set(new_topos)


	print('New topologies found:')
	for nt in new_topos:
		print(nt)


