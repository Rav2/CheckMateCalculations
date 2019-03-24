# 24.03.2019

# This analysis was devoted to create a 4-dimensional grid of points and test if the software works well. In addition, total SUSY x-section was calculated using Pythia.

# **RESULTS DISCARDED** due to bug in CheckMATE (read below)

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 433
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE
**luminosity:** 36 fb^-1

## *Steps:*
0. Use UML/grid/generation.py script to generate a grid of points.
1. Use UML/gen_slha.sh to generate slha files
2. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
3. Copy SLHA files to the cluster
4. Use make_divide_lists.sh to create lists of SLHA files
4. While using tmux command, run udocker_scripts/jobs_inner.sh or  udocker_scripts/jobs_inner_parallel.sh to call auto_checkmate_cluster_pythia.sh script with appropriate parameters: all SUSY processes, and all 13 TeV analyses. This version of script will call first CheckMATE with Pythia for 1k events. Then it will use xsection/reuse_pythia.py to parse Pythia log file and calculate the rough estimate of total SUSY cross-section. Then CheckMATE will be run again with a new value of events to calculate.
5. Merge results using collect_results.py.
6. Plot results using plot_all.py in this folder.

## *Result:*
There is a bug with providing the number of events to be simulated by Pythia as a command line argument for CheckMATE. Therefore all results were in fact calculated for 10k events, no matter what was the actual cross-section. It should be possible to provide the argument using Pythia cards. However, the accuracy of Pythia calculations is questionable.
