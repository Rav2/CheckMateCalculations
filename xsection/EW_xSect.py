#!/usr/bin/python
# This script calls for EWKfast_LO and calculates the total cross-section for SUSY weak sector
# This script takes three arguments: path to EWKfast_LO.py script, path to SLHA file, exact path to results folder
#
import subprocess
import sys
import os.path

def main(ewk_path, slha_path, resdir):
	# run EWKfast_LO and catch output
	output = None
	try:
		output = subprocess.check_output([ewk_path, slha_path])
	except subprocess.CalledProcessError as e:
		output = e.output.decode('utf8').strip()
		print('[ERROR] EWKfast_LO reported an error. Here goes the output:')
		print(output)
		exit(1)
	# write output to file
	text_file = open(os.path.join(resdir, "EWK.txt"), "wb")
	text_file.write(output)
	text_file.close()
	# parse output to get the total EW cross-section
	xSect = 0.0
	# decode bytes to string object
	output = output.decode('utf8').strip().split("\n")
	for line in output:
		#remove duplicate white spaces
		" ".join(line.split())
		line = line.split()
		# len(line) is 0 for blank lines
		if len(line) > 0 and line[0].isdigit():
			xSect += float(line[4])
	return xSect

if __name__ == '__main__':
	# check for arguments
	assert len(sys.argv) == 4, "[ERROR] Use: ./EW_xSect.py [EWKFast.py path] [SLHA path] [RESDIR path]"
	xSect = main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
	print("[INFO] Total EW cross-section: {}".format(xSect))
