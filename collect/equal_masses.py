#!/usr/bin/python
#
# This scripts reads collect_nev.txt and searches for points for which mG is equal to mQ or mQ3, then produces a list of slha files
#

path = '/RESULTS/grid4D/in_files/'
prefix = 'grid'
slha_list = []

with open('collective_nev.txt', 'r') as f:
	for line in f:
		line = line.split()
		mG = line[0]
		if mG == line[1] or mG == line[2] or mG == line[3]:
			slha_list.append(path+prefix+'_'+mG+'_'+line[1]+'_'+line[2]+'_'+line[3]+'.slha')

with open('list.txt', 'w') as f:
	for line in slha_list:
		f.write(line+'\n')