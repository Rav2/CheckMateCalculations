#!/usr/bin/env python
#
#
import sys
import os.path
import write_pythia_input

script_path=os.path.dirname(os.path.realpath(__file__))

ifseed = '#'
ifxsect = '#'
ifsxescterr = '#'
try:
	name = str(sys.argv[1]).replace('\"','').strip()
	analyses = str(sys.argv[2]).replace('\"','').strip()
	energy = str(sys.argv[3])
	slha = str(sys.argv[4])
	quiet = str(sys.argv[5]).replace('\"','').strip()
	seed = int(sys.argv[6])
	if seed >= 0:
		ifseed = ''
	outdir = str(sys.argv[7])
	nev = int(sys.argv[8])
	xsections = float(sys.argv[9])
	xsecterr = float(sys.argv[10])
	processes = str(sys.argv[11]).replace('\"','').strip()
	card_dir = str(sys.argv[12])

except:
    print '[name] [analyses] [energy] [slha] [quiet] [seed] [outdir] [nev] [xsections] [xsecterr] [processes] [card dir]'
    exit()

processes = [str(x).strip() for x in processes.split(',')]
xsections = [float(x) for x in str(xsections).split(',')]
xsecterr = [float(x) for x in str(xsecterr).split(',')]

proper_xsections = True
for xs in xsections:
	if xs < 0.0:
		proper_xsections = False
if proper_xsections:
	assert len(processes) == len(xsections) and len(xsections) == len(xsecterr), "[ERROR] The no of processes must match the no of x-sections and x-section errors!"
else:
	sys.stderr.write("[WARNING] Provided cross-sections have negative values!\n")

process_blocks = ''
for it, proc in enumerate(processes):
	jj = it
	p8card = write_pythia_input.main(slha, proc, energy, nev)
	p8path = os.path.join(card_dir, name + "_" + proc + ".in")
	p8file = open(p8path, 'w')
	p8file.write(p8card)
	p8file.close()
	if proper_xsections:
		ifxsect = ''
		ifsxescterr = ''
	else:
		ifxsect = '#'
		ifsxescterr = '#'
		jj=0



	process_blocks += """
[process{}]
Pythia8Card: {}
	""".format(it+1, p8path)


print '''
[Parameters]
Name: {name}
Analyses: {analyses}

#### CheckMATE results should be stored in the following directory
OutputDirectory: {outdir}

#### In case target output directory already exists, do the following
####   Overwrite old directory
OutputExists: Overwrite

####   Keep the old results and add the below (either as a new process, which adds to the signal prediction, or as an already existing process to add statistics)
# OutputExists: Add

####   Always ask (standard)
# OutputExists: Ask

#### Don't print output on screen
QuietMode: {quiet}

#### Avoids the input query and starts CheckMATE straight away if the input setup is valid
# SkipParamCheck: True

#### Don't do any detector simulation (useful if one only wants to create Pythia .hepmc files)
# SkipDelphes: True

#### Don't do any analysis step (useful if one only wants to create Delphes .root files)
# SkipAnalysis: True

#### Don't do any evaluation (in case one just wants the analysis result)
# SkipEvaluation: True

#### Calculate signal efficiency for each signal region
# EffTab: True

#### Calculate CLs for all signal regions of all tested analyses (can take a long time)
# FullCLs: True

#### Calculate CLs for the signal region with the largest r-value
# BestCLs: 5

#### Calculate simplified likelihood for each signal region
# Likelihood: True

#### Provide a SUSY-LesHouches spectrum in case one wants to generate events with Pythia8
SLHAFile: {slha}

#### If Pythia8 is used for event generation, store the intermediate .hepmc file
# WritePythiaEvents: False

#### If Delphes runs, store the intermediate .root file
# WriteDelphesEvents: False

#### Tell Delphes that some new BSM particles are invisible
# InvisiblePIDs: 35, 36

#### Specify RandomSeed of all CheckMATE components to get deterministic results
{ifseed}RandomSeed: {seed}

#### Store _unevaluated_ results for each  event and each process 
#EventResultFileColumns: analysis, sr, signal_normevents, signal_err_stat, signal_err_sys, signal_err_tot
#ProcessResultFileColumns: analysis, sr, signal_normevents, signal_err_stat, signal_err_sys, signal_err_tot

#### Store evaluated overall result and per-analysis
#TotalResultFileColumns: analysis, sr, obs, bkg, bkgerr, S95obs, S95exp, robscons, rexpcons, robsconssysonly, rexpconssysonly, CLsobs, CLsexp
#BestPerAnalysisResultFileColumns: analysis, sr, obs, bkg, bkgerr, S95obs, S95exp, robscons, rexpcons, CLsobs, CLsexp

#### Process Information (Each new process 'X' must start with [X])
{process_blocks}


'''.format(name=name, analyses=analyses, outdir=outdir, quiet=quiet, slha=slha, ifseed=ifseed, seed=seed, process_blocks=process_blocks)
