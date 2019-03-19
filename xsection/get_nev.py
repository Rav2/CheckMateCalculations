#!/usr/bin/python
# This script calls for EWKfast_LO and  NLLFast, calculates the total cross-section for SUSY and number of events required for NMC
# It requires 5 arguments: path to minimum number of events to simulate, EWKfast executable, path to SLHA file, path to NLLFast executable, string with parameters for NLLFAST
# exact path to results dir for given model point
#
import sys
import math
import subprocess
import os
import EW_xSect
import NLLFast_xSect
import pyslha

# check for arguments
assert len(sys.argv) == 6, "[ERROR] Use: ./get_nev.py [minimum nev] [EWKFast.py path] [SLHA path] [NLFast path] [RESDIR path]"

def parse_SLHA(slha_file):
	slha = pyslha.read(slha_file)
	d = {}
	d['mg'] = slha.decays[1000021].mass
	d['mdL'] = slha.decays[1000001].mass
	d['mdR'] = slha.decays[2000001].mass
	d['muL'] = slha.decays[1000002].mass
	d['muR'] = slha.decays[2000002].mass
	d['msL'] = slha.decays[1000003].mass
	d['msR'] = slha.decays[2000003].mass
	d['mcL'] = slha.decays[1000004].mass
	d['mcR'] = slha.decays[2000004].mass
	d['mb1'] = slha.decays[1000005].mass
	d['mb2'] = slha.decays[2000005].mass
	d['mt1'] = slha.decays[1000006].mass
	d['mt2'] = slha.decays[2000006].mass
	d['mQ'] = 1.0/8.0 * (d['mdL'] + d['mdR'] + d['muL'] + d['muR'] + d['msL'] + d['msR'] + d['mcL'] + d['mcR'])
	return d

def main():
	L=36. # luminosity fb^-1
	f=10. # boost factor
	pdf="mstw" # partition distribution function used for NLLFast
	processes = ["gg", "sg", "ss", "sb", "st"]
	xsect_ewk = 0.0
	xsect_nll = 0.0
	masses = parse_SLHA(sys.argv[3])
	try:
		# calculate cross-section for EW sector
		xsect_ewk = EW_xSect.main(sys.argv[2], sys.argv[3], sys.argv[5])
		# calculate cross-section for strong sector, for each process
		for pp in processes:
			if pp in ("gg", "sg", "ss", "sb"):
				arg = pp + " " + pdf + " " + str(int(masses['mQ'])) + " " + str(int(masses['mg']))
				xsect_nll += NLLFast_xSect.main(sys.argv[4], arg, sys.argv[5])
			elif pp=="st":
				mm = [masses['mt1'], masses['mt2'], masses['mb1'], masses['mb2']]
				for mass in mm:
					arg = pp + " " + pdf + " " + str(int(mass))
					xsect_nll += NLLFast_xSect.main(sys.argv[4], arg, sys.argv[5])
			else:
				print("[WARNING] Unsupported mode: "+pp)
	except subprocess.CalledProcessError as e:
		output = str(e.output)
		print('[ERROR] NLLFast or EWKfast reported an error. Here goes the output:')
		print(output)
		exit(1)
	total_xsect = xsect_nll + xsect_ewk
	print("[INFO] Total SUSY cross-section: {} pb".format(total_xsect))
	# multiply by 1000 because x-section in pb and luminosity in fb^-1
	nev_calc = int(f * total_xsect * 1000 * L)+1
	print("[INFO] Required no of events: {}".format(nev_calc))
	nev = max(nev_calc, int(sys.argv[1]))
	print("[INFO] No of events to simulate: {}".format(nev))
	# write output to a file
	txt_output = """Luminosity: {} fb^-1
Boost factor: {}
EWK cross-section: {} pb
NLLFast cross-section: {} pb
Total cross-section: {} pb
Minimal number of events to simulate: {}
Calculated number of events to simulate: {}
Number of events to simulate: {} """.format(L, f, xsect_ewk, xsect_nll, total_xsect, sys.argv[1], nev_calc, nev)

	text_file = open(os.path.join(sys.argv[5], "total_xsect.txt"), "w")
	text_file.write(txt_output)
	text_file.close()

	return nev
	
if __name__ == '__main__':
	nev = main()
	sys.stderr.write(str(nev)+'\n')


