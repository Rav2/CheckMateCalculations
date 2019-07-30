#!/usr/bin/env python
# This script generates a grid for CMSSM model scanning m0 and m1/2

import os, sys
import numpy as np

n0 = 22 # no of points for m0
n12 = 15 # no of points for m1/2
#tanB = [5, 40]
tanB = [40]
# for m0 in [int(x) for x in np.linspace(100, 3000, n0)]:
#     for mhalf in [int(x) for x in np.linspace(400, 1200, n12)]:
#         for tanval in tanB:
#             for A0 in [0, -mhalf]:
#                 for sign in [+1, -1]:
#                     print("{}\t{}\t{}\t{}\t{}".format(m0, mhalf, tanval, A0, sign))
for m0 in [int(x) for x in np.linspace(400, 9000, n0)]:
    for mhalf in [int(x) for x in np.linspace(400, 3000, n12)]:
        for tanval in tanB:
            for A0 in [-mhalf]:#[0, -mhalf]:
                for sign in [1]:#[+1, -1]:
                    print("{}\t{}\t{}\t{}\t{}".format(m0, mhalf, tanval, A0, sign))


