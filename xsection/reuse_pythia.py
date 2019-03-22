#!/usr/bin/python
#
# This scripts parses pythia log and calculates the total cross-section for all SUSY processes.
#
import sys

def main(log_path):
	with open(log_path, "r") as file:
		begin = -1000
		reading = False
		xsect = 0.0
		for no,line in enumerate(file):
			# detect the beginning of the block
			if "PYTHIA Process Initialization" in line and not "End" in line:
				begin = no
			# detect the beginning of useful information and start reading
			elif no == begin+11:
				reading = True
			if reading:
				# detect the end of useful information, end the work
				if " |                                                                  |" in line:
					reading = False
					xsect = xsect * 10**12
					print("[INFO] Total SUSY cross-section is {} fb\n".format(xsect))
					return xsect
				else:
					words = line.split()
					xx = None
					try:
						xx = float(words[-2])
					except ValueError:
						print("[ERROR] SLHA parser failed at line: {}, parsing the line: '{}\n'".format(no, words))
						exit(1)
					xsect += xx 

if __name__ == '__main__':
	# check for arguments
	assert len(sys.argv) == 2, "[ERROR] Use: ./reuse_pythia.py [path to pythia log file]\n"
	L = 36. # fb^-1
	f = 10.
	xs = main(sys.argv[1]) # fb
	nev = int(f*L*xs) +1
	print("[INFO] Calculated no of events: {}\n".format(nev))
	sys.stderr.write(str(nev)+'\n')

