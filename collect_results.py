#!/usr/bin/python

# Script to collect results from the directory (and its subdirs) provided as an argument.

import os
import sys
import os.path
import re

silent = False # change to True to silence all info output

if not silent:
	print ("[START]")

if len(sys.argv) != 2:
	print("[ERROR] Wrong parameter! Type: ` ./collect_results.py <path_to_results_dir> `")
	exit(1)

if not silent:
	print("[INFO] Collecting results from {0}".format(sys.argv[1]))

results = []
prefix = ""
comment=""
# pattern = re.compile('Result for r: [\s=]+([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$')
# loop over files
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in [f for f in filenames if f=="result.txt"]:
    	dir_name = os.path.split(dirpath)[1].split('_')
    	prefix = dir_name[0]
    	line = ''
    	for ii,val in enumerate(dir_name[1:]):
    		line = line +val+'\t'
    		comment = comment + "par"+str(ii)+'t'
    	comment = comment + 'r'
    	print(os.path.join(dirpath, filename))
    	with open(os.path.join(dirpath, filename), 'r') as f:
    		for fline in f:
    			if "Result for r:" in fline:
    				r = fline.split(' ')[-1]
        			line += r
    				results.append(line)

if not silent:
	print("[INFO] Preparing to save results...")
out_file_path = os.path.join(sys.argv[1], 'collective_results_' + prefix + '.txt')
exists = os.path.isfile(out_file_path)

ii = 1
while exists:
	out_file_path = os.path.join(sys.argv[1], 'collective_results' + prefix + '({0}).txt'.format(ii))
	exists = os.path.isfile(out_file_path)
	ii += 1

if not silent:
	print("[INFO] Writing results to a text file {}: ".format(out_file_path))

with open(out_file_path, 'a') as the_file:
    the_file.write("# Combined results from the directory {0}\n".format(sys.argv[1]))
    the_file.write(comment)
    for res in results:
    	the_file.write(res)

if not silent:
	print("[END]")


