# !/bin/bash

SOFTSUSY="/Users/rafalmaselek/ScienceSoft/softSUSY"
INFILE="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/grid/gridCMSSM.dat"
OUTDIR="/Users/rafalmaselek/Projects/CheckMateCalculations/UML/SLHA_SOFT"
PREFIX="cmssm"
MODEL="sugra"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"	#directory of bash script

if [[ ! -d "$OUTDIR" ]]; then
	mkdir $OUTDIR
	if [[ ! -e "$OUTDIR" || ! -d "$OUTDIR" ]]; then
		echo "[ERROR] Could not create directory for output!"
		exit 1
	fi
fi

echo "[INFO] Running softSUSY..."
SOFTSUSY_EXEC="${SOFTSUSY}"/bin/softpoint.x 

#sugra --m0=1000 --m12=1200 --a0=-100 --tanBeta=20 --sgnMu=-1
while IFS= read -r LINE
do
	ARR=($LINE)
	NAME="${PREFIX}_${ARR[0]}_${ARR[1]}_${ARR[2]}_${ARR[3]}_${ARR[4]}"
	echo ${NAME}
	${SOFTSUSY_EXEC} ${MODEL} --m0=${ARR[0]} --m12=${ARR[1]} --tanBeta=${ARR[2]} --a0=${ARR[3]} --sgnMu=${ARR[4]} > ${OUTDIR}/${NAME}.slha
  	#echo ${ARR[0]}
done < "$INFILE"
