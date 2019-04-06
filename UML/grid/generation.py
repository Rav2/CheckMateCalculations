#!/usr/bin/env python

import os, sys
import numpy as np

n = 10 # full grid
# n = 3 # mini grid

mG_ar = np.logspace(np.log10(1000.1), np.log10(3000.1), n)
mQ_ar = np.logspace(np.log10(1000.1), np.log10(3000.1), n)
mQ3_ar = np.logspace(np.log10(500.1), np.log10(3000.1), n)

print '# mG mQ mQ3 mN1'
for mG in mG_ar:
    for mQ in mQ_ar:
        for mQ3 in mQ3_ar:
            mmin = min([mG, mQ, mQ3])
            nn1 = 5 + int( 10.1 * np.log(mmin/200.)/np.log(3500./200.) ) # full grid
            #nn1 = 2 + int( 5.1 * np.log(mmin/200.)/np.log(3500./200.) )  # mini grid

            mdiff_ar = np.logspace(np.log10(10.), np.log10(mmin), nn1)
            for mdiff in mdiff_ar:
                mn1 = mmin - mdiff 
                if mn1 == 0: mn1 = 1
                m = map(int, [mG, mQ, mQ3, mn1])                
                print m[0], m[1], m[2], m[3] 

