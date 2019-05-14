#!/usr/bin/env python
# This script generates a grid for CMSSM model scanning m0 and m1/2

import os, sys
import numpy as np

n = 15 # no of points for m0 and m1/2 scan
tanB = [5, 40]

for m0 in [int(x) for x in np.linspace(1000, 3000, n)]:
    for mhalf in [int(x) for x in np.linspace(400, 1200, n)]:
        for tanval in tanB:
            for A0 in [0, -mhalf]:
                for sign in [+1, -1]:
                    print("{}\t{}\t{}\t{}\t{}".format(m0, mhalf, tanval, A0, sign))



