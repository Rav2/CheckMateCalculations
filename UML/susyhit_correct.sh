# !/bin/bash

SUSYHIT="/Users/rafalmaselek/susyhit/run"
INDIR="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA"
OUTDIR="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_FIX"
PREFIX=""


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"	#directory of bash script

if [[ ! -d "$OUTDIR" ]]; then
	mkdir $OUTDIR
	if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
		echo "[ERROR] Could not create directory for output!"
		exit 1
	fi
fi

echo "[INFO] Running SUSYHit..."
SUSYHIT_DIR=$(echo `dirname $SUSYHIT`)
for FILE in $INDIR/$PREFIX*.slha; do
	FILE=$(echo `basename $FILE`)
	cp $INDIR/$FILE $SUSYHIT_DIR/slhaspectrum.in
	cd $SUSYHIT_DIR
	./$(echo `basename $SUSYHIT`)
	cp susyhit_slha.out $OUTDIR/$FILE
	cd $DIR
done