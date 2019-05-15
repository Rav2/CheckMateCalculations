#!/usr/bin/python
import sys
import os

def main(in_path):
	prefix = 'cmssm'
	changed = []
	changed_files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(in_path):
		for file in f:
			with open(os.path.join(r, file), 'r') as of:
				if len(file) < 5 or file[0:5] != 'cmssm':
					print('{} not recognised, skipping!'.format(file))
					continue
				pars = [float(x) for x in file.split('.')[0].split('_')[1:]]
				assert(len(pars) == 5)
				content = of.readlines()
				pars_new = [None, None, None, None, None]
				for ii,line in enumerate(content):
					if '# m0' in line:
						val = float(line.strip().split()[1])
						pars_new[0] = val
					elif '# m12' in line:
						val = float(line.strip().split()[1])
						pars_new[1] = val
					elif '# tanb' in line:
						val = float(line.strip().split()[1])
						pars_new[2] = val
					elif '# A0' in line:
						val = float(line.strip().split()[1])
						pars_new[3] = val
					elif '# sign(mu)' in line:
						val = float(line.strip().split()[1])
						pars_new[4] = val
				if pars != pars_new:
					changed.append('{} -> {}\n'.format(pars, pars_new))
					changed_files.append(file+'\n')
					os.rename(os.path.join(r, file), os.path.join(r, file.replace(prefix, 'broken')))

	with open('changed.txt', 'w') as wf:
		wf.write('(m0, mhalf, tanB, A0, sign) -> AFTER SUSYHIT\n')
		wf.writelines(changed)
	with open('excluded.txt', 'w') as wf:
		wf.writelines(changed_files)

if __name__ == '__main__':
	path = './SLHA_FIX'
	if len(sys.argv) == 2:
		path = sys.argv[1]
	main(path)