#!/bin/bash
# 
# This script is used to submit jobs on the Kruk cluster
FILE_PATH="/RESULTS/minigrid4D/lists"
FILE_NAME="minigrid"

NO_START=391
NO_END=395
STEP=1

for (( IT = $NO_START; IT <= $NO_END; IT += $STEP ))
	do
        #NODE=$(( $IT % 10 + 11 ))
		ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
		qsub -N $FILE_NAME"_["$IT"]" -l host='w61|w62|w63|w64' -v arg=$ARG /home/2/rm394969/udocker-1.1.3/usetting.sh
		#/home/2/rm394969/udocker-1.1.3/skrypt.sh $ARG
	done


