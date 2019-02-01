# 01.02.2019

# This analysis was devoted to reproduce exclusion plots from atlas analysis: 1712_02332 https://arxiv.org/abs/1712.02332 figures 13.a and 13.b were reproduced it was an initial test of doing calculations on the cluster

## *Steps:*
0. Make sure paths specified in input_path.txt are valid.
1. Run make_slha.sh, where grid and analysis is specified. It will use modified version of LHC_recast, in particular main_sms_RM.sh.
2. Copy files to udocker.
3. Use divide_list.sh to create files with short lists of SLHA files to proceed by CheckMATE.
4. Use udocker scripts to make jobs assigning list files to auto_checkmate_cluster_p8cards.sh script.
5. Merge results using collect_results.py.
6. Plot results using scripts in this folder.

## *Result:*
Two reproduced exclusion plots for QqN1 and GqqN1 processes. Plots have approximately 10k points each. The r-value is indicated as a color of the points. Plots are OK.

## *Notes:*

### *Problems:*
1. Some points are missing due to very old kernel at some nods.

### *Solutions:*
1. Jobs are assigned only to nodes that are for sure OK, i.e. w11-w20. Emanuele promised to help by making a new container. Paweł K. is not responding.

### *TODO:*
1. Make bands on the curve.
2. Make general scripts for writing, reading and plotting results for N-dimensional space of parameters.
