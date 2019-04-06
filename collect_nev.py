#!/usr/bin/python

# Script to collect nev from the directory (and its subdirs) provided as an argument. It reads xsect.txt files.

import os
import sys
import os.path
import re

silent = False # change to True to silence all info output

if not silent:
	print ("[START]")

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print("[ERROR] Wrong parameter! Type: ` ./collect_results.py <path_to_results_dir> [path_to_in_file_dir]`")
	exit(1)

if not silent:
	print("[INFO] Collecting nev from {0}".format(sys.argv[1]))

results = []

FILES = 0
# loop over files
par_no = 0
done = set()
alls = set()
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
	alls.add(os.path.split(dirpath)[1])
	for filename in [f for f in filenames if f=="xsect.txt"]:
		done.add(os.path.split(dirpath)[1])
		dir_name = os.path.split(dirpath)[1].split('_')
		line = ''
        # read parameters from directory's name
		for ii,val in enumerate(dir_name[1:]):
			line = line +val+'\t'
        # determine the no of parameters
		if par_no == 0:
			par_no = len(line.split('\t')) - 1
    	# print(os.path.join(dirpath, filename))
		with open(os.path.join(dirpath, filename), 'r') as f:
			FILES += 1
			for fline in f:
				if "xsect" in fline:  
					xsect = fline.replace('xsect=(', '').replace(') mb', '').replace(' +- ', '\t').replace('\n', '')
					line += xsect + '\t'
				elif "nev" in fline:
					nev = fline.replace('nev=', '')
					line +=  nev + '\n'
			results.append(line)

undone = alls - done
if len(sys.argv) == 3:
	if not silent:
		print("[INFO] Listing unstarted SLHA file to: {}".format(os.path.join(sys.argv[1], 'unstarted' + '.txt')))
	with open( os.path.join(sys.argv[1], 'unstarted' + '.txt'), 'w') as file:
		for em in undone:
			if em != '' :
				path = os.path.join(sys.argv[2], em + '.slha\n')
				file.write(path)

comment="# "
for ii in range(par_no) :
    comment = comment + "par"+str(ii+1)+'\t'
comment = comment + 'xsect [mb]\txsecterr [mb]\tnev\n'

if not silent:
	print("[INFO] Preparing to save nev...")
out_file_path = os.path.join(sys.argv[1], 'collective_nev' + '.txt')
exists = os.path.isfile(out_file_path)

ii = 1
while exists:
	out_file_path = os.path.join(sys.argv[1], 'collective_nev' + '({0}).txt'.format(ii))
	exists = os.path.isfile(out_file_path)
	ii += 1

if not silent:
	print("[INFO] Writing results to a text file {} ".format(out_file_path))

with open(out_file_path, 'a') as the_file:
    the_file.write("# Combined nev from the directory {0}\n".format(sys.argv[1]))
    the_file.write(comment)
    for res in results:
    	the_file.write(res)

if not silent:
	print("[INFO] {} xsect files found!".format(FILES))

if not silent:
	print("[END]")


