#!/usr/bin/env python

import os, sys

print('''#
#
BLOCK SPINFO  # Spectrum Program information
     1   SuSpect     # RGE +Spectrum calculator
     2   2.41        # version number
# nothing to signal: output a priori reliable
#
BLOCK MODSEL  # Model selection
     1     1   #SUGRA                                             
#
BLOCK MINPAR  # Input parameters
         1     {}   #  m0                 
         2     {}   #  m_1/2              
         3     {}   #  tanbeta(mZ)        
         4     {}   #  sign(mu)           
         5     {}   #  A0                 
#
BLOCK EXTPAR  # Input parameters
         0     7.28047708E+03   # EWSB scale          
#
BLOCK SMINPUTS  # Standard Model inputs
         1     1.27934000E+02   # alpha_em^-1(M_Z)^MSbar
         2     1.16639000E-05   # G_F [GeV^-2]
         3     1.17200000E-01   # alpha_S(M_Z)^MSbar
         4     9.11870000E+01   # M_Z pole mass
         5     4.25000000E+00   # mb(mb)^MSbar
         6     1.72500000E+02   # mt pole mass
         7     1.77710000E+00   # mtau pole mass

'''.format(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[5]), float(sys.argv[4])))