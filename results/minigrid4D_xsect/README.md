# 24.03.2019

# This analysis was devoted to create a 4-dimensional grid of points and test if the software works well. In addition, total SUSY x-section was calculated using NLLfast and EWKfast.

# **RESULTS DISCARDED** due to problems with NLLfast (read below)

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 433
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using x-section from NLLfast and EWKfast
**luminosity:** 36 fb^-1

## *Steps:*
0. Use UML/grid/generation.py script to generate a grid of points.
1. Use UML/gen_slha.sh to generate slha files
2. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
3. Copy SLHA files to the cluster
4. Use make_divide_lists.sh to create lists of SLHA files
4. While using tmux command, run udocker_scripts/jobs_inner.sh or  udocker_scripts/jobs_inner_parallel.sh to call xsection/auto_checkmate_cluster_nll.sh script with appropriate parameters: all SUSY processes, and all 13 TeV analyses. This version of script will call scripts from xsection/ folder to calcualte total SUSY cross-section using NLLfast and EWKfast. Ensure that you have the software installed and appropriate paths are in *input_paths.txt*.
5. Merge results using collect_results.py.
6. Plot results using plot_all.py in this folder.

## *Result:*
Calculations were aborted, because the problem with NLLfast was found. NLLfast is based on prepared grid, for which there exists an upper limit on squark masses. The limit was exceeded by my grid. It is possible to use NLLfast anyways, but some discontinuity effects would occur. The nexe idea was to use Pythia to estimate the no of events to simulate.

