# !/bin/bash
# By Rafal Maselek rafalmaselek@gmail.com
# This script takes two arguments, the path to a file containing the list of paths to Pythia card files and path to output folder.
# It divides the list into smaller pieces and writes it into separate files.
#___________________________________

# How many paths put into one file:
SPLIT=5
# Output where files will be written
OUTDIR=""

FILE=""
if [ $# -ne 2 ]; then
    echo "[ERROR] Wrong arguments supplied! Provide a path to a txt file with list of paths and path to output folder!"
    exit 1 
else
	FILE=`echo $1`
	if [[ ! -e "$FILE" ]]; then
		echo "[ERROR] The input file doesn't exist!"
		exit 1
	fi
	OUTDIR=`echo $2`
	#Check if output directory exists
	if [[ ! -d "$OUTDIR" ]]; then
		mkdir $OUTDIR
		if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
			echo "[ERROR] Could not create directory for output!"
			exit 1
		fi
	fi

fi

NAME="$(echo `basename $FILE` | cut -d'.' -f1)"
LINE_NO=0
CURR_FILE=""
NO=0
cd $OUTDIR
while IFS= read -r LINE || [[ -n "$LINE" ]]; do
	if [[ $(($LINE_NO % $SPLIT)) == 0 ]]; then
		NO="$(( $LINE_NO / $SPLIT ))"
		CURR_FILE=$NAME"_[$NO].txt"
		if [[ -e "$CURR_FILE" ]]; then
			rm $CURR_FILE
		fi
	fi
	echo $LINE >> $CURR_FILE
	LINE_NO=$(($LINE_NO + 1))

done < "$FILE"
echo "[INFO] $(( $NO + 1 )) files created."