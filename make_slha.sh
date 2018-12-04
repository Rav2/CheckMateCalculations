#!/bin/bash

LHC_RECAST_PATH='/Users/rafalmaselek/Projects/LHC_recast'
RESULT_PATH='/Users/rafalmaselek/TEMP'
MODE="QqN1"
ANALYSIS="atlas_1712_02332"

M1_MIN=500
M1_MAX=1200
M1_STEP=200

M2_MIN=500
M2_MAX=1500
M2_STEP=200

#Check if output directory exists
if [[ ! -d "$RESULT_PATH" ]]; then
	mkdir $RESULT_PATH
	if [[ ! -e "$RESULT_PATH" || ! -d "$RESULT_PATH" ]]; then
		echo "[ERROR] Could not create directory for data!"
		exit 1
	fi
fi
#Check if subdirectory exists
if [[ ! -d "$RESULT_PATH/in_files" ]]; then
	mkdir $RESULT_PATH/in_files
	if [[ ! -e "$RESULT_PATH/in_files" || ! -d "$RESULT_PATH/in_files" ]]; then
		echo "[ERROR] Could not create directory for in files!"
		exit 1
	fi
fi
#Check if subdirectory exists
if [[ ! -d "$RESULT_PATH/output" ]]; then
	mkdir $RESULT_PATH/output
	if [[ ! -e "$RESULT_PATH/output" || ! -d "$RESULT_PATH/output" ]]; then
		echo "[ERROR] Could not create directory for results!"
		exit 1
	fi
fi

#run main_sms scripts to create pythia setting files and slha files
cd $LHC_RECAST_PATH
for (( m1 = $M1_MIN; m1 <= $M1_MAX; m1 += $M1_STEP ))
	do
		for (( m2 = $M2_MIN; m2 <= $M2_MAX; m2 += $M2_STEP ))
			do
				bash $LHC_RECAST_PATH/main_sms_RM.sh $RESULT_PATH $ANALYSIS $MODE $m1 $m2 
			done
	done	