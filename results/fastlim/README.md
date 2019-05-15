# 15.05.2019

# This analysis scans the space of CMSSM parameters checking the total SUSY coverage 

**energy:** 13 TeV
**processes:** allSUSY
**model parameters:**  mG, mQ, mQ3, mN1
**no of points:** 2640 -> 2591
**generator:** no need
**cross-sections:** susy-cross-section python package by Sho Iwamoto and EWKfast_LO
**seed:** random
**no of events:** not-applicable
**luminosity:** ?

## *Steps:*
0. Use UML/grid/generationCMSSM.py script to generate a grid of points. 
    Limits used:
    * m0: (100, 3000, 22)
    * m12: (400, 1200, 15)
    * tanB: {5, 40}
    * A0: {0. -m12}
    * sign: {-1, 1}
1. Use UML/gen_slhaCMSSM.sh to generate slha files
2. Use UML/softsusy_slha.sh to call softSUSY to calculate particles' masses
3. Use UML/susyhit_correct.sh to correct SLHA files using susyhit
4. Use UML/fastlim.sh to call fastlim.py and perform computations
6. Plot results using plot.py in this folder, omitting files with errors

## *Result:*
* plots/proc contains histograms, one shows how many times each process had the top coverage, second shows how many times each process was in the top 3 processes according to SUSY coverage
* plots/rate contains 2D plots in m0 vs m12 coordinates. Color corresponds to the coverage value of the best process.
* plots/xsec contains 2D plots in m0 vs m12 coordinates. Color corresponds to the cross-section value of the best process with rescpect to SUSY coverage.

## *Problems:*
1. Some points (around 50, mostly small values of m0) did not pass the susyhit step. Susyhit have thrown a fortran error, similar to the ones seen before.
2. Some points have a "branching ration differs from 1" issue. If one of the BRs was 0, fastlim calculations crashed due to division by 0 error. If it was greater than zero, calculations continued, but such points have not been plotted.
