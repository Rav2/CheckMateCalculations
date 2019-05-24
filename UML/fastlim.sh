# !/bin/bash

FASTLIM="/Users/rafalmaselek/Projects/fastlim-1.0/fastlim.py"
INDIR="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
OUTDIR="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/FASTLIM_OUT"
PREFIX="cmssm"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"	#directory of bash script

if [[ ! -d "$OUTDIR" ]]; then
	mkdir $OUTDIR
	if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
		echo "[ERROR] Could not create directory for output!"
		exit 1
	fi
fi

echo "[INFO] Running Fastlim..."
for FILE in $INDIR/$PREFIX*.slha; do
	NAME=$(basename $FILE)
	echo ${NAME}
	NAME=${NAME/slha/"txt"}
	# echo $NAME
	python3 ${FASTLIM} ${FILE} > ${OUTDIR}/${NAME}	
done
