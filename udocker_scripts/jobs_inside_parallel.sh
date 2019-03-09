#!/bin/bash
#
# Script to call CheckMate multiple times from inside of udocker environment.
# It calls several processes of CheckMate parallel and monitors the number of processes.
# This scripts allows for faster calculations but the usage of the node is bigger.

FILE_PATH="/RESULTS/minigrid4D/lists"
FILE_NAME="minigrid"

NO_START=401
NO_END=433
STEP=1

MAX_PROCESSES=30

IT=$NO_START
until [[ $IT > $NO_END ]]; do
  NO=$( echo $( ps | wc -l ) )
  if [[ $NO < $MAX_PROCESSES ]]; then
  	echo "processes: "${NO} "iterator: "${IT}
  	ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
  	/CheckMATECalculations/auto_checkmate_cluster.sh $ARG &
    IT=$(( $IT + $STEP ))
  fi
  sleep 1 # add this to prevent thrashing with ps
done



