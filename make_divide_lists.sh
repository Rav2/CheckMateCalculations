# !/bin/bash
# By Rafal Maselek rafalmaselek@gmail.com
# This script takes three arguments, prefix name of output files, the path to a folder containing input files and path to output folder.
# PROVIDE ABSOLUTE PATHS!
# It writes lists with paths to files. Names of output files start with the name provided as 1st argument
#___________________________________

# How many paths put into one file:
SPLIT=4
# Output where files will be written
OUTDIR=""
EXT="slha"
NAME="name"
INDIR=""
if [ $# -ne 3 ]; then
    echo "[ERROR] Wrong arguments supplied! ./make_divide_list.sh <NAME> <INDIR> <OUTDIR>"
    exit 1 
else
	NAME=`echo $1`
	INDIR=`echo $2`
	if [[ ! -d "$INDIR" ]]; then
		echo "[ERROR] The input folder doesn't exist!"
		exit 1
	fi
	if [ ${INDIR: -1} == "/" ]; then
		size=$(( ${#INDIR} - 1))
		INDIR=${INDIR: 0: $size }
	fi
	OUTDIR=`echo $3`
	#Check if output directory exists
	if [[ ! -d "$OUTDIR" ]]; then
		mkdir $OUTDIR
		if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
			echo "[ERROR] Could not create directory for output!"
			exit 1
		fi
	fi

fi
# echo "INDIR: $INDIR"
# echo "OUTDIR: $OUTDIR"

IT=0
CURR_FILE=""
shopt -s nullglob
for file in $INDIR/*.$EXT 
do
	cd $OUTDIR
	if [[ $(($IT % $SPLIT)) == 0 ]]; then
		NO="$(( $IT / $SPLIT + 1))"
		CURR_FILE=$NAME"_[$NO].txt"
		if [[ -e "${CURR_FILE}" ]]; then
			rm $CURR_FILE
		fi
	fi
	echo $file >> "${CURR_FILE}"

	IT=$(($IT + 1))
done
echo "[INFO] $(( $NO )) files created."