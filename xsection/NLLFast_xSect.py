#!/usr/bin/python
# This script calls for NLLFAST and calculates the total cross-section for SUSY strong sector
# This script takes three arguments: path to NLLFast executable, string with arguments for NLLFast, exact path to results folder
#
import subprocess
import sys
import os.path

def main(nll_path, nll_args, resdir):
	# run EWKfast_LO and catch output
	args = [arg for arg in nll_args.split()]
	output = None
	# try executing the NLLFAST program
	try:
		curr_path = os.getcwd()
		nll_path = os.path.dirname(os.path.abspath(nll_path))
		nll_exec = os.path.join(".", os.path.basename(os.path.abspath(nll_path)))
		os.chdir(nll_path)
		output = subprocess.check_output([nll_exec] + args)
		os.chdir(curr_path)
	except subprocess.CalledProcessError as e:
		output = '[ERROR] NLLFast reported an error. Here goes the output:\n' + e.output.decode('utf8').strip()
		print(output)		
		exit(1)
	# write output to a file
	text_file = open(os.path.join(resdir, "NLLFast.txt"), "ab")
	text_file.write(output)
	text_file.close()
	# parse output to get the total cross-section
	xSect = 0.0
	# decode bytes to string object
	output = output.decode('utf8').strip().split("\n")
	for ii,line in enumerate(output):
		#remove duplicate white spaces
		" ".join(line.split())
		line = line.split()
		if ii == 4:
			xSect += float(line[3])
	return xSect

if __name__ == '__main__':
	# check for arguments
	assert len(sys.argv) == 4, "[ERROR] Use: ./NLFast_xSect.py [NLFast path] [NLFast params as single str] [RESDIR path]"
	xSect = main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
	print("[INFO] Total NLL+NLO[pb] cross-section: {}".format(xSect))

