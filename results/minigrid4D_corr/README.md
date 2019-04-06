# 6.04.2019

# This analysis was devoted to create a 4-dimensional grid of points and test if the software works well. In addition, total SUSY x-section was calculated using Pythia.

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 247
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE
**luminosity:** 36 fb^-1

## *Steps:*
0. Use UML/grid/generation.py script to generate a grid of points. 
    Limits used:
    * mG: (700, 3500)
    * mQ: (500, 3500)
    * mQ3: (200, 3500)
    * mN1: default log-like generation
1. Use UML/gen_slha.sh to generate slha files
2. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
3. Copy SLHA files the apropriate directory (/RESULTS/minigrid4D_corr/in_files)
4. Use make_divide_lists.sh to create lists of SLHA files
4. Run udocker_scripts/tmux.sh to create a tmux session for every 10 list files executed by Jobs.sh script (renamed to jobs_tmux.sh)
5. Merge results using collect_results.py.
6. Plot results using plot_all.py in this folder.

## *Result:*
* **collective_results.txt** -- total results containing for each minigrid point: the value of r parameter, LO cross-section with its error and the number of events to simulate. The last three values come from the initial pre-run in which Pythia was called to generate 1000 events.s
* 51 plots showing the slices of 4-dimensional grid along the N1 direction (3D part of 4D space corresponding to particular value of N1 mass). Three axes correspond to values of three mass parameters. Color of the points represents the value of r factor.
* Ditribution of the number of events to simulate
