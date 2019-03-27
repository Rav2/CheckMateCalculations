#!/usr/bin/python -u
#
# This scripts parses pythia log and calculates the total cross-section for all SUSY processes.
#
import sys
import os.path

# check for arguments
assert len(sys.argv) == 3, "[ERROR] Use: ./reuse_pythia.py [path to pythia log file] [path to resdir]\n"

# Parameters
L = 36. # fb^-1
f = 10.

xsect = 0.0
xsecterr = 0.0
with open(sys.argv[1], "r") as file:
	for no,line in enumerate(file):
		if "| sum" in line:
			line = line.strip().split()
			xsect = float(line[-3])
			xsecterr = float(line[-2])
			print("[INFO] Total SUSY cross-section: {} +- {} mb".format(xsect, xsecterr))
nev = int(f*L*xsect*10**12) +1
print("[INFO] Calculated no of events: {}".format(nev))

output="""L={L} fb^-1
f={f}
xsect=({xsect} +- {xsecterr}) mb
nev={nev}""".format(L=L, f=f, xsect=xsect, xsecterr=xsecterr, nev=nev)

dirpath = sys.argv[2]
filepath = os.path.join(dirpath, "xsect.txt")
print("[INFO] Writing xsection to {}".format(filepath))
with open(filepath, 'w') as f:
	f.write(output)
	f.flush()
# sys.stdout.flush()
sys.stderr.write(str(nev)+'\n')

