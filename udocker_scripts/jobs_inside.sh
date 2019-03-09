#!/bin/bash
#
# Script to call CheckMate multiple times from inside of udocker environment.
FILE_PATH="/RESULTS/minigrid4D/lists"
FILE_NAME="minigrid"

NO_START=341
NO_END=400
STEP=1

for (( IT = $NO_START; IT <= $NO_END; IT += $STEP ))
	do
		ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
		/CheckMATECalculations/auto_checkmate_cluster.sh $ARG
	done


