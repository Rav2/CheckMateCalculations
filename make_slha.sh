#!/bin/bash
# By Rafal Maselek rafalmaselek@gmail.com
# In this script one can specify the analysis, mode and lattice. It will call other scripts that will create Pythia settings files
# as well as one file named MODE_ANALYSIS.txt containing a list of paths to all Pythia card files.
# The script takes no arguments.
LHC_RECAST_PATH='/Users/rafalmaselek/Projects/LHC_recast'
RESULT_PATH='/Users/rafalmaselek/TEMP'
if [[ -e "input_paths.txt" ]]; then
	echo "[INFO] Reading paths from input_paths.txt"
	exec 4< "input_paths.txt"
	line_no=0
	while IFS= read -r LINE<&4 || [[ -n "$LINE" ]]; do
		LINE="$(echo -e "${LINE}" | sed -e 's/[[:space:]]*$//')"
		if [[ !( "$LINE" =~ ^#.*$ ) ]]; then
			line_no=$(($line_no + 1))
			if [[ $line_no == 3 ]]; then
				LHC_RECAST_PATH=$LINE
			elif [[ $line_no == 4 ]]; then
				RESULT_PATH=$LINE	
			fi
		fi
	done
	exec 4<&-
	echo "[INFO] LHC_RECAST PATH:    $LHC_RECAST_PATH"
	echo "[INFO] PYTHIA CARDS DIR:   $RESULT_PATH"
else
	echo "[WARNING] File: input_paths.txt NOT FOUND! Using default paths."
fi
########################################

MODE="QqN1"
ANALYSIS="atlas_1712_02332"

M1_MIN=400
M1_MAX=1600
M1_STEP=12

M2_MIN=0
M2_MAX=700
M2_STEP=12

echo "[INFO] Mode selected: $MODE"
echo "[INFO] Analysis selected: $ANALYSIS" 
echo "[INFO] LATTICE: ($M1_MIN, $M1_MAX, $M1_STEP) ($M2_MIN, $M2_MAX, $M2_STEP)"
echo "[INFO] Checking the existence of directories..."
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

#run main_sms scripts to create pythia setting files 
echo "[INFO] Generating Pythia setting files"
echo "_______________________________________________"
cd $LHC_RECAST_PATH
for (( m1 = $M1_MIN; m1 <= $M1_MAX; m1 += $M1_STEP ))
	do
		for (( m2 = $M2_MIN; m2 <= $M2_MAX; m2 += $M2_STEP ))
			do
				bash "$LHC_RECAST_PATH/main_sms_RM.sh" $RESULT_PATH $ANALYSIS $MODE $m1 $m2 
			done
	done
