..
#!/bin/bash
#
# Script to call CheckMate multiple times from inside of udocker environment.
# It calls several processes of CheckMate parallel and monitors the number of processes.
# This scripts allows for faster calculations but the usage of the node is bigger.
#######################################################

# SCRIPT PARAMETERS
#######################################################
# PATH TO THE RESULT FOLDER CONTAINING SUBFOLDER lists/ WITH LISTS OF SLHA FILES
MY_PATH="/RESULTS/minigrid4D_ch2cards"
# PREFIX OF THE NAMES OF LISTS
FILE_NAME="minigrid"
# WHICH LISTS TO COMPUTE
NO_START=58
NO_END=433
STEP=1
# MAXIMUM NUMBER OF PROCESSES IN ps COMMAND
MAX_PROCESSES=2000

# SCRIPT BODY
######################################################
FILE_PATH=$MY_PATH"/lists"
LOG_PATH=$MY_PATH"/logs"

# CREATE LOG DIRECTORY
if [[ ! -d "$LOG_PATH" ]]; then
	echo "Creating directory for logs"
	mkdir $LOG_PATH
	if [[ ! -e "$LOG_PATH" || ! -d "$LOG_PATH" ]]; then
		echoerr "[ERROR] Could not create directory $LOG_PATH !"
		exit 1
	fi
fi


IT=$NO_START
until [[ $(( $IT - $NO_END )) -gt 0 ]]; do
  NO=$( ps | wc -l )
 # echo "Loop with NO="$NO
  if [[ $(( $NO - $MAX_PROCESSES)) -lt 0 ]]; then
  	echo "processes: "$NO "iterator: "$IT
  	ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
  	/CheckMATECalculations/auto_checkmate_cluster_ch2cards.sh $ARG >$LOG_PATH"/log_["$IT"].txt" 2>&1 &
# /dev/null 2>&1 &  #$LOG_PATH"/log_["$IT"].txt" 2>&1 &
	IT=$(( $IT + $STEP ))
  fi
  sleep 2 # add this to prevent thrashing with ps
done

echo "WORK DONE!!!"
