# 25.06.2019

# This analysis was devoted to create a 4-dimensional grid of points -- Universal Mass Limit.
In addition, total SUSY x-section was calculated using Pythia.

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 10181
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE, not less than 1000
**luminosity:** 36 fb^-1

## *Steps:*
0. Use UML/grid/generation.py script to generate a grid of points. 
    Limits used:
    * mG: (1000, 3000)
    * mQ: (1000, 3000)
    * mQ3: (200, 3500)
    * mN1: default log-like generation, from 1 up, maintaining N1 LSP
1. Use UML/gen_slha.sh to generate slha files
2. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
3. Copy SLHA files the apropriate directory (/RESULTS/grid4D/in_files)
4. Use make_divide_lists.sh to create lists of SLHA files
4. Run udocker_scripts/tmux.sh to create a tmux session for every 10 list files executed by Jobs.sh script (renamed to jobs_tmux.sh)
5. Merge results using collect_results.py.
6. Plot results using plot_all.py in this folder.

## *Result:*
* **collective_results.txt** -- total results containing for each grid point: the value of r parameter, LO cross-section with its error and the number of events to simulate. The last three values come from the initial pre-run in which Pythia was called to generate 1000 events.s
* 10 plots showing the mQ vs mQ3 vs mN1 and r value, each plot corresponds to mG slice
* Ditribution of the number of events to simulate
