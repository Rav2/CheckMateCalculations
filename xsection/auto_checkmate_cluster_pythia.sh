#!/bin/bash

#--------------------------------------#
#---- AUTO_CHECKMATE BY R. MASELEK ----#
#--------------------------------------#

#---- Script parameters
SILENT='false'	#set to true to disable all script generated output to stdout
DEBUG='true' 	#set to 'true' to prevent deleting the directory with standard CheckMATE output
NAME='' #tag-name of the files
PARAMS="-a 13TeV -q -oe overwrite" 	#parameters for checkmate
PROCESS="allsusy"	#process for pythia
MIN_NEV=1000	#minimal number of events to simulate
CALC_XSECT='true' #set to 'true' to calculate required no of events using NLLfast and EWKfast

echo $PARAMS
#---- Function for printing messages to stdout
inside_print()
{
	if ! [[ $SILENT == 'true' ]]; then
		echo ${1}
	fi
}
#---- Function for printing messages to stderr
echoerr() { echo "$@" 1>&2; }

clear
inside_print "[START]"

#---- Paths to executables
cd "$( dirname "${BASH_SOURCE[0]}" )"
if [[ -e "input_paths.txt" ]]; then
	inside_print "[INFO] Reading paths from input_paths.txt"
	exec 4< "input_paths.txt"
	CHECKMATE=""
	SUSYHIT=""
	PREFIX=""
	OPT=0
	while IFS= read -r LINE<&4 || [[ -n "$LINE" ]]; do
		LINE="$(echo -e "${LINE}" | sed -e 's/[[:space:]]*$//')"
		if [[ !( "$LINE" =~ ^#.*$ ) ]]; then
			if [[ $OPT -eq 1 ]]; then
				CHECKMATE=$LINE
			elif [[ $OPT -eq 2 ]]; then
				SUSYHIT=$LINE
			elif [[ $OPT -eq 3 ]]; then
				PREFIX=$LINE
			fi
		else 
			if [[ "$LINE" = *"CHECKMATE"*  ]]; then
				OPT=1
			elif [[ "$LINE" = *"SUSYHIT"* ]]; then
				OPT=2
			elif [[ "$LINE" = *"RESULTS"* ]]; then
				OPT=3
			else 
				OPT=0
			fi
		fi
	done
	exec 4<&-
else
	inside_print "[INFO] Reading paths from script"
	CHECKMATE=/Users/rafalmaselek/CheckMATE-2.0.26/bin/CheckMATE
	SUSYHIT=/Users/rafalmaselek/susyhit/run
	PREFIX="/RESULTS/4DIM/MINIGRID"
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
RESDIR=$PREFIX'/results'		#where to place results (NO "/"" AT THE END) 
OUTDIR=$PREFIX'/output'		#where to place temporary files (NO "/"" AT THE END)
INDIR=$PREFIX'/in_files'		#where to look for Pythia cards (NO "/"" AT THE END)

inside_print "[INFO] RESDIR: $RESDIR"
inside_print "[INFO] OUTDIR: $OUTDIR"
inside_print "[INFO] INDIR: $INDIR"
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
	cp $2 $RESDIR/$1
	cp $OUTDIR/$1/result.txt $OUTDIR/$1/evaluation/best_signal_regions.txt $OUTDIR/$1/evaluation/total_results.txt \
	$OUTDIR/$1/pythia/pythia_process.log $RESDIR/$1
	if [[ CALC_XSECT == 'true' ]]; then
		cp $OUTDIR/$1/EWK.txt $RESDIR/$1
	fi
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
	echo "IMPORTANT! To run auto_checkmate you need to have a .txt file named 'input_paths.txt'"
	echo "in the same folder as the script. To see how the file should look like, use the"
	echo "'input_paths_template.txt' file."
	echo ""
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
	exit 1
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
		make_dir ${RESDIR}/${NAME} 
		inside_print "[INFO] Running CheckMATE..."
		PARAMS2=$( echo '-slha' ${FILE} '-od' ${OUTDIR} )
		NEV=${MIN_NEV}
		if [[ $CALC_XSECT=='true' ]]; then
			# make a dry run to estimate the total SUSY x-section
			$CHECKMATE -n ${NAME} ${PARAMS} ${PARAMS2} -pyp "p p > $PROCESS" -maxev ${NEV}
			# calculate required no of events to simulate
			output=$(./xsection/reuse_pythia.py ${OUTDIR}"/"${NAME}"/pythia/pythia_process.log" 2>&1)
			# print calculated x-section
			inside_print "[${output#*[}"
			array=( $output )
			NEV=${array[0]}
			if [[ ${MIN_NEV} -gt ${NEV} ]]; then
				NEV=${MIN_NEV}
				inside_print "[INFO] No of event to simulate: ${NEV}" 
			fi
		fi
	    $CHECKMATE -n ${NAME} ${PARAMS} ${PARAMS2} -pyp "p p > $PROCESS" -maxev ${NEV}
		move_results $NAME $FILE
	fi
else
#---- CASE 4: User provides a single file with names of slha files in it
	inside_print "[INFO] Reading names of SLHA files from: $FILE"
	#---- read input file line by line to extract file names
	while read -r LINE <&3 || [[ -n "$LINE" ]]; do
		inside_print "[INFO] Text read from input file: $LINE"
	    if ! [[ ${LINE: -5} == ".slha" ]]; then
			LINE=$LINE.slha
	    fi
		NAME=$(echo `basename $LINE` | cut -d'.' -f1)
		make_dir ${RESDIR}/${NAME} 
	    inside_print "[INFO] Running CheckMATE..."
		PARAMS2=$( echo '-slha' ${LINE} '-od' ${OUTDIR} )
		NEV=${MIN_NEV}
		if [[ $CALC_XSECT=='true' ]]; then
			# make a dry run to estimate the total SUSY x-section
			$CHECKMATE -n ${NAME} ${PARAMS} ${PARAMS2} -pyp "p p > $PROCESS" -maxev ${NEV}
			# calculate required no of events to simulate
			output=$(./xsection/reuse_pythia.py ${OUTDIR}"/"${NAME}"/pythia/pythia_process.log" 2>&1)
			# print calculated x-section
			inside_print "[${output#*[}"
			array=( $output )
			NEV=${array[0]}
			if [[ ${MIN_NEV} -gt ${NEV} ]]; then
				NEV=${MIN_NEV}
				inside_print "[INFO] No of event to simulate: ${NEV}" 
			fi
		fi
	    $CHECKMATE -n ${NAME} ${PARAMS} ${PARAMS2} -pyp "p p > $PROCESS" -maxev ${NEV}
		move_results $NAME $FILE
	done 3<"$FILE"
fi

inside_print "[END]"
