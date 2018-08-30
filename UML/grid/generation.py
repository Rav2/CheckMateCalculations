#!/usr/bin/env python

import os, sys
import numpy as np

mG_ar = np.logspace(np.log10(700.1), np.log10(3500.1), 15)
mQ_ar = np.logspace(np.log10(500.1), np.log10(3500.1), 15)
mQ3_ar = np.logspace(np.log10(200.1), np.log10(3500.1), 15)

print '# mG mQ mQ3 mN1'
for mG in mG_ar:
    for mQ in mQ_ar:
        for mQ3 in mQ3_ar:
            mmin = min([mG, mQ, mQ3])
            nn1 = 5 + int( 10.1 * np.log(mmin/200.)/np.log(3500./200.) )
            mdiff_ar = np.logspace(np.log10(10.), np.log10(mmin), nn1)
            for mdiff in mdiff_ar:
                mn1 = mmin - mdiff 
                if mn1 == 0: mn1 = 1
                m = map(int, [mG, mQ, mQ3, mn1])                
                print m[0], m[1], m[2], m[3] 

