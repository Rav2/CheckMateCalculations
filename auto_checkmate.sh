#!/bin/bash

#--------------------------------------#
#---- AUTO_CHECKMATE BY R. MASELEK ----#
#--------------------------------------#

#---- Script parameters
SILENT='false' 		  #set to true to disable all script generated output to stdout
USE_FILE_NAMES='false' #set 'true' to use file names to name output folders in multi-file mode instead of using natural numbers
DEBUG='false' #set to 'true' to prevent deleting the directory with standard CheckMATE output

#---- CheckMATE basic parameters
PYTHIA='allsusy'		#which process to simulate
ANALYSES='atlas_1802_03158'	#which analyses to perform
NEV='5000'			#max number of events
OUTDIR='./results'		#where to place results (NO "/"" AT THE END)
INDIR='./res/example_input'	#where to look for SLHA files if a list of names is provided (NO "/"" AT THE END)

#---- CheckMATE additional parameters
PARAMS='-q'

#---- Function for printing messages to stdout
inside_print()
{
	if ! [[ $SILENT == 'true' ]]; then
		echo $1
	fi
}
#---- Function for printing messages to stderr
echoerr() { echo "$@" 1>&2; }

clear
inside_print "[START]"

#---- Paths to executables
if [[ -e "input_paths.txt" ]]; then
	exec 4< "input_paths.txt"
	read  CHECKMATE<&4
	read  SUSYHIT<&4
	exec 4<&-
	inside_print "[INFO] Reading paths from input_paths.txt"
else
	inside_print "[INFO] Reading paths from script"
	CHECKMATE=/Users/rafalmaselek/CheckMATE-2.0.26/bin/CheckMATE
	SUSYHIT=/Users/rafalmaselek/susyhit/run
fi

##############################################################################
make_output_dir()
{
	if [[ ! -d "$OUTDIR" ]]; then
		mkdir $OUTDIR
		if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
			echoerr "[ERROR] Could not create directory for results!"
			exit 1
		fi
	fi
}

#---- Working area
FILE=`echo $1`						#input file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"	#directory of bash script
OUTPUT_EXISTS='overwrite'				#what to do if output already exists 


# the temp directory used, within $DIR
# omit the -p parameter to create a temporal directory in the default location
WORK_DIR=$(mktemp -d $DIR/tmp_XXXXXXXX)

# check if tmp dir was created
if [[ ! -d "$WORK_DIR" ]]; then
  echoerr "[ERROR] Could not create temp dir! Close the terminal and try again!"
  exit 1
else
  inside_print "[INFO] Temporary directory created:  $WORK_DIR"
fi

# deletes the temp directory
function cleanup() 
{      
  rm -rf "$WORK_DIR" 
  inside_print "[INFO] Deleted temp working directory $WORK_DIR"
  inside_print ""
}

#---- register the cleanup function to be called on the EXIT signal
if ! [[ $DEBUG == 'true' ]]; then
	trap cleanup EXIT 
fi
#create results directory if it doesn't exist
make_output_dir

#---- Functions
# run SUSYHit and copy the output to WORK_DIR
susyhit()
{
	inside_print "[INFO] Running SUSYHit..."
	local SUSYHIT_DIR=$(echo `dirname $SUSYHIT`)
	cp $INDIR/$1 $SUSYHIT_DIR/slhaspectrum.in
	cd $SUSYHIT_DIR
	./$(echo `basename $SUSYHIT`)
	cp susyhit_slha.out $WORK_DIR/$1
	cd $DIR
}

# create a convenient folder hierarchy and move interesting files in it 
move_results()
{
	cd $OUTDIR
	II=1
	DEST=$1
	if [[ ! -d "$1" ]]; then
		mkdir $1
		if [[ ! -d "$1" ]]; then
			echoerr "[ERROR] Could not create subdirectory for name: $1"
			exit 1
		fi
	else
		while [[ -d "$1_$II" ]]; do
			II=$((II+1))
		done
		mkdir $(echo "$1_$II")
		DEST=$(echo "$1_$II")
		echo "[WARNING] Results for: $1 will be saved as $1_$II!"

	fi
	cp $WORK_DIR/$2 $WORK_DIR/$1
	cp $WORK_DIR/$1/result.txt $WORK_DIR/$1/evaluation/best_signal_regions.txt $WORK_DIR/$1/evaluation/best_signal_regions.txt \
$WORK_DIR/$1/evaluation/total_results.txt $WORK_DIR/$1/pythia/pythia_process.log $WORK_DIR/$1/$2 ./$DEST
	cd $DIR
}

# print help to stdout
print_help()
{
	SILENT='true'
	echo ""
	echo "[HELP]"
	echo "auto_checkmate allows running SUSYHit with CheckMATE for one or many slha files at once."
	echo "To use it, provide as an argument a path to a single slha file, or alternatively"
	echo "to a text file containing names of slha files (one per line, files in the same folder"
	echo "as the list-file)."
	echo ""
}

# validate if input file provided to SUSYHit looks like a proper SLHA file
validate_slha()
{
	./slha_validator.py  $INDIR/$1
	if [ $? != 0 ]; then
		echoerr "[ERROR] SLHA input file is broken!"
		exit 1
	fi
}

#---------------------------------#
#---- THE MAIN PART OF SCRIPT ----#
#---------------------------------#

#---- CASE 0: User provides no arguments
if [ $# -eq 0 ]; then
    echoerr "[ERROR] No arguments supplied! Type ./auto_checkmate --help for help!"
    exit 1 
#---- CASE 1: User asks for help
elif [[ $FILE == "-h" || $FILE == "--help" ]] ; then
	print_help
	exit 0
#---- CASE 2: User provides wrong flag
elif [ ${FILE: 0:1} == "-" ]; then
	echoerr "[ERROR] Unknown flag! Type ./auto_checkmate --help for help!"
	exit 1
#---- CASE 3: User provides a single SLHA file as a parameter
elif [ ${FILE: -5} == ".slha" ]; then
	if [[ ! -e $FILE ]]; then
    		echoerr "[ERROR] SLHA file: $FILE doesn't exist!"
    		exit 1
	else 
		NAME=$(echo `basename $FILE` | cut -d'.' -f1)
		INDIR=$(dirname $FILE)
		validate_slha $NAME.slha
		susyhit $NAME.slha
		inside_print "[INFO] SUSYHit done. Running CheckMATE..."
		$CHECKMATE -n $NAME -pyp "p p > $PYTHIA" -a $ANALYSES -maxev $NEV -slha $WORK_DIR/$NAME.slha -oe $OUTPUT_EXISTS -od $WORK_DIR $PARAMS
		move_results $NAME $NAME.slha
	fi
else
#---- CASE 4: User provides a single file with names of SLHA files in it
	inside_print "[INFO] Reading names of SLHA files from: $FILE"
	IT=1
	OUTDIR=$OUTDIR/$(echo `basename $FILE` | cut -d'.' -f1)
	make_output_dir
	#---- read input file line by line to extract slha file names
	while read -r LINE <&3 || [[ -n "$LINE" ]]; do
		inside_print "[INFO] Text read from input file: $LINE"
	    if ! [[ ${LINE: -5} == ".slha" ]]; then
			LINE=$LINE.slha
	    fi
	    validate_slha $LINE
	    susyhit $LINE
	    NAME=$(echo $LINE | cut -d'.' -f1)
	    IT_NAME=$(printf '%i' $IT )
	    if [[ $USE_FILE_NAMES == 'true' ]]; then 
	    	IT_NAME=$NAME
	    	if [[ -d $OUTDIR/$NAME ]]; then
	    		echo "[WARNING] Results for: $NAME will be overwritten!"
	    	fi
	    fi
	    inside_print "[INFO] SUSYHit done. Running CheckMATE..."
	    $CHECKMATE -n $IT_NAME -pyp "p p > $PYTHIA" -a $ANALYSES -maxev $NEV -slha $WORK_DIR/$LINE -oe $OUTPUT_EXISTS -od $WORK_DIR $PARAMS
		move_results $IT_NAME $LINE
		if ! [[ $USE_FILE_NAMES == 'true' ]]; then 
			IT=$((IT+1)) 
		fi
	done 3<"$FILE"
fi

inside_print "[END]"
