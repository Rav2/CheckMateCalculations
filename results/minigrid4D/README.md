# 09.03.2019

# This analysis was devoted to create a 4-dimensional grid of points and test if the software works well

## *Steps:*
0. Use UML/grid/generation.py script to generate a grid of points.
1. Use UML/gen_slha.sh to generate slha files
2. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
3. Copy SLHA files to the cluster
4. Use make_divide_lists.sh to create lists of SLHA files
4. Run udocker_scripts/jobs_inner.sh or  udocker_scripts/jobs_inner_parallel.sh to call auto_checkmate_cluster.sh script with appropriate parameters: all SUSY processes, and all 13 TeV analyses
5. Merge results using collect_results.py.
6. Plot results using plot_all.py in this folder.

## *Result:*
6 plots showing r value for all possible pairs out of four parameters (mG, mQ, mQ3, mN1).

## *Notes:*

### *Problems:*
1. Plots look strange, discuss with Kazuki.
2. Still not able to use the full power of cluster, only single node using ssh.

### *Solutions:*
1.
2. Find a way to talk with P. K. In the meantime use udocker_scripts/jobs_inside_parallel.sh to speed up calculations. What about Emanuele?

### *TODO:*
