#!/bin/bash
#
# This script is called by jobs.sh. It loads udocker environment and calls for CheckMate

# print some nod info
echo "[KERNEL] $(uname -r)"
hostname

# load udocker and call CheckMate
/home/2/rm394969/udocker-1.1.3/udocker.py run --hostauth --user=rm394969 \
		--nometa \
		--workdir / \
		-v /home/2/rm394969/CheckMATE:/CheckMATE \
		-v /home/2/rm394969/CheckMateCalculations-master:/CheckMATECalculations \
		-v /home/2/rm394969/susyhit:/susyhit \
                -v /home/2/rm394969/SLHA:/SLHA \
		-v /home/2/rm394969/LHC_recast-master:/LHC_recast \
		-v /home/2/rm394969/EWKfast_LO:/EWKfast_LO \
		-v /home/2/rm394969/NLLfast:/NLLfast \
		 LHCrecasting /bin/bash /CheckMATECalculations/auto_checkmate_cluster.sh $arg