# 09.03.2019

# This analysis was devoted to create a 4-dimensional grid of points and test if the software works well

**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 433
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit
**seed:** random
**no of events:** Pythia?

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
1. Around 30 points were missing. The calculations was redone with a random seed. Old results have a suffix "old" in the names of files.
2. Find a way to talk with P. K. In the meantime use udocker_scripts/jobs_inside_parallel.sh to speed up calculations. What about Emanuele?
Update 13.03.2019: Together with P. K. we solved the problem. I have modified udocker_scripts/jobs_inside_parallel.sh and now with the help of **tmux** command, I am able to calculate many points in a parallel way. Mr P. K. assigned me one of the nodes for personal use.

**Using tmux command:**
1. Login to cluster.
2. Login to private node via ssh protocol.
3. Type *tmux* to open a new console.
4. Do your stuff, e.g. enter udocker and run calculations.
5. Press **Ctrl+b** and then **d** to exit tmux console without stopping the calculations.
6. You can go back to the sessions by using command *tmux attach*.
7. To kill the sessions exit it by **Ctrl+d** (you might need to press it several times).
Tmux command allows to do stuff on computers connected to with ssh protocol, without the need to be logged in all the time.

***NOTE:*** To calculate many points, processes were sent to background using ampersand *&* at the end of command.

### *TODO:*
