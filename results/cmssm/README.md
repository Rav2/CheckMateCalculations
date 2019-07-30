# 14.07.2019

# This analysis was devoted to perform 2D scan for cMSSM model and compare it with UML scan

## CMS PART
**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  m0, m1/2, tanB, A0, signMu
**no of points:** 2591
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slhaCMSSM.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE, not less than 1000
**luminosity:** 36 fb^-1

### *Steps:*
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

### *Result:*
* **data/cmssm.txt** -- total results containing for each grid point: the value of r parameter, LO cross-section with its error and the number of events to simulate. The last three values come from the initial pre-run in which Pythia was called to generate 1000 events.

## UML part
**analyses:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 10181
**generator:** Pythia in CheckMate
**cross-sections:** UML/write_slha.py script + SUSYhit -> Pythia in CheckMATE
**seed:** random
**no of events:** calculated using Pythia in CheckMATE, not less than 1000
**luminosity:** 36 fb^-1

### *Steps:*
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

### *Result:*
* **data/UML.txt** -- total results containing for each grid point: the value of r parameter, LO cross-section with its error and the number of events to simulate. The last three values come from the initial pre-run in which Pythia was called to generate 1000 events.

## Combination
1. UML results were loaded.
2. RandomForestClassifier was trained on UML data.
3. cMSSM data was loaded and plotted.
4. For each point from cMSSM data, the values of parameters were used to find appropriate SLHA file, then four UML masses were found for every point.
5. Four masses was used to classify CMSSM point using the previously trained model.
6. Based on new classification, another exclusion contour was added to plots.

### Results:
* 8 plots, each showing the distribution of r value for 5D parameter space of cMSSM in m0 vs m1/2 planes. Each plot contains an exclusion contours for this data and for UML-based estimation.
