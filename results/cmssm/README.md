# 25.06.2019

# This analysis was devoted to perform 2D scan for cMSSM model

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  m0, m1/2, tanB, A0, signMu
**no of points:** 2591
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slhaCMSSM.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE, not less than 1000
**luminosity:** 36 fb^-1

## *Steps:*
0. Use UML/grid/generationCMSSM.py script to generate a grid of points. 
    Limits used:
    * m0: (100, 3000)
    * m1/2: (400, 1200)
    * tanB: {0, 40}
    * A0: {0, -m1/2}
    * signMu: {-1, 1}
1. Use UML/gen_slhaCMSSM.sh to generate slha files
2. Use UML/softsusy_slha.sh to generate particle spectrum
3. Use UML/susyhit_correct.sh to calculate decay channels
4. Use UML/detect_changeCMSSM.py to detect if there are any problematic points
5. Copy SLHA files the apropriate directory (/RESULTS/cmssm/in_files)
6. Use make_divide_lists.sh to create lists of SLHA files
7. Run udocker_scripts/tmux.sh to create a tmux session for every 10 list files executed by Jobs.sh script (renamed to jobs_tmux.sh)
8. Merge results using collect_results.py.
9. Plot results using plot_all.py in this folder.

## *Result:*
* **collective_results.txt** -- total results containing for each grid point: the value of r parameter, LO cross-section with its error and the number of events to simulate. The last three values come from the initial pre-run in which Pythia was called to generate 1000 events.s
* 8 exclusion plots showing m0 vs m1/2 and r value, each of the plot corresponds to one of the 8 combinations of tanB, A0 and signMU parameters