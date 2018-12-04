#!/bin/bash

#--------------------------------------#
#---- AUTO_CHECKMATE BY R. MASELEK ----#
#--------------------------------------#

#---- Script parameters
SILENT='false' 		  #set to true to disable all script generated output to stdout
USE_FILE_NAMES='true' #set 'true' to use file names to name output folders in multi-file mode instead of using natural numbers
DEBUG='false' #set to 'true' to prevent deleting the directory with standard CheckMATE output

NAME='' #tag-name of the files
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
make_dir()
{
	if [[ ! -d "$1" ]]; then
		mkdir $1
		if [[ ! -e "$1" || ! -d "$1" ]]; then
			echoerr "[ERROR] Could not create directory $1 !"
			exit 1
		fi
	fi
}

#---- Working area
FILE=`echo $1`	#input file
WORK_DIR=$(dirname $(dirname $FILE) )

#---- Directories 
RESDIR=$WORK_DIR'/results'		#where to place results (NO "/"" AT THE END) 
OUTDIR=$WORK_DIR'/output'		#where to place temporary files (NO "/"" AT THE END)
INDIR=$WORK_DIR'/in_files'		#where to look for SLHA files (NO "/"" AT THE END)

#--- Creating directories
make_dir $RESDIR
make_dir $OUTDIR
make_dir $INDIR

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"	#directory of bash script

# deletes the WORKDIR 
function cleanup() 
{      
  rm -rf "$OUTDIR/$NAME" 
  inside_print "[INFO] Deleted working directory $OUTDIR/$NAME"
  inside_print ""
}

#---- register the cleanup function to be called on the EXIT signal
if ! [[ $DEBUG == 'true' ]]; then
	trap cleanup EXIT 
fi

#---- Functions
# run SUSYHit and copy the output to WORK_DIR
susyhit()
{
	inside_print "[INFO] Running SUSYHit..."
	# local SUSYHIT_DIR=$(echo `dirname $SUSYHIT`)
	# cp $INDIR/$1 $SUSYHIT_DIR/slhaspectrum.in
	# cd $SUSYHIT_DIR
	# ./$(echo `basename $SUSYHIT`)
	# cp susyhit_slha.out $WORK_DIR/$1
	# cd $DIR
}

# create a convenient folder hierarchy and move interesting files in it 
move_results()
{
	cd $RESDIR
	if [[ ! -d "$1" ]]; then
		mkdir $1
		if [[ ! -d "$1" ]]; then
			echoerr "[ERROR] Could not create subdirectory for name: $1"
			exit 1
		fi
	fi
	cp $INDIR/$2 $RESDIR/$1
	cp $OUTDIR/$1/result.txt $OUTDIR/$1/evaluation/best_signal_regions.txt $OUTDIR/$1/evaluation/total_results.txt \
	$OUTDIR/$1/pythia/pythia_process.log $RESDIR/$1
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
# validate_slha()
# {
# 	./slha_validator.py  $INDIR/$1
# 	if [ $? != 0 ]; then
# 		echoerr "[ERROR] SLHA input file is broken!"
# 		exit 1
# 	fi
# }

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
#---- CASE 3: User provides a single card file as a parameter
elif [ ${FILE: -4} == ".dat" ]; then
	if [[ ! -e $FILE ]]; then
    		echoerr "[ERROR] DAT file: $FILE doesn't exist!"
    		exit 1
	else 
		NAME=$(echo `basename $FILE` | cut -d'.' -f1)
		# INDIR=$(dirname $FILE)
		# validate_slha $NAME.slha
		# susyhit $NAME.slha
		# inside_print "[INFO] SUSYHit done."
		inside_print "[INFO] Running CheckMATE..."
		$CHECKMATE $FILE
		move_results $NAME $NAME.spcdec
	fi
else
# #---- CASE 4: User provides a single file with names of parameter cards in it
	inside_print "[INFO] Reading names of parameter cards from: $FILE"
# 	IT=1
# 	OUTDIR=$OUTDIR/$(echo `basename $FILE` | cut -d'.' -f1)
# 	make_output_dir
# 	#---- read input file line by line to extract file names
	while read -r LINE <&3 || [[ -n "$LINE" ]]; do
		inside_print "[INFO] Text read from input file: $LINE"
	    if ! [[ ${LINE: -4} == ".dat" ]]; then
			LINE=$LINE.dat
	    fi
# 	    validate_slha $LINE
# 	    # susyhit $LINE
	    # NAME=$(echo $LINE | cut -d'.' -f1)
# 	    IT_NAME=$(printf '%i' $IT )
# 	    if [[ $USE_FILE_NAMES == 'true' ]]; then 
# 	    	IT_NAME=$NAME
# 	    	if [[ -d $OUTDIR/$NAME ]]; then
# 	    		echo "[WARNING] Results for: $NAME will be overwritten!"
# 	    	fi
# 	    fi
# 	    # inside_print "[INFO] SUSYHit done."
		NAME=$(echo `basename $LINE` | cut -d'.' -f1)
	    inside_print "[INFO] Running CheckMATE..."
	    $CHECKMATE $LINE
		move_results $NAME $NAME.spcdec
# 		if ! [[ $USE_FILE_NAMES == 'true' ]]; then 
# 			IT=$((IT+1)) 
# 		fi
	done 3<"$FILE"
fi

inside_print "[END]"
