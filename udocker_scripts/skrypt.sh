#!/bin/bash
#
# This script loads udocker environment. To use in interactive mode on cluster.

/home/2/rm394969/udocker-1.1.3/udocker.py run --hostauth --user=rm394969 \
		--nometa \
		--workdir / \
		--env="DISPLAY" \
		-v /home/2/rm394969/CheckMATE:/CheckMATE \
		-v /home/2/rm394969/CheckMateCalculations-master:/CheckMATECalculations \
		-v /home/2/rm394969/susyhit:/susyhit \
                -v /home/2/rm394969/SLHA:/SLHA \
		-v /home/2/rm394969/LHC_recast-master:/LHC_recast \
		-v /home/2/rm394969/EWKfast_LO:/EWKfast_LO \
		-v /home/2/rm394969/NLLFast:/NLLFast \
		-v /home/2/rm394969/SYS_SCRIPT:/SYS_SCRIPT \
		-v /home/2/rm394969/fastlim_results:/fastlim_results \
		 LHCrecasting /bin/bash -rcfile /SYS_SCRIPT/on_start.sh 

