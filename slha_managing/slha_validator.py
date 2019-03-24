#!/usr/bin/env python
# @author: Rafal Maselek
# @email: rafalmaselek@gmail.com
# The following script checks, if the SLHA file provided 
# as a command line argument has correct SLHA structure.
# To run this script a pyslha module is required. Install it by pip.
import pyslha
import sys

try:
	d = pyslha.read(sys.argv[1])
except:
	sys.exit(1)

