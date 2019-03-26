#!/bin/bash
#

function absolute_path()
{
	echo "$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
}	


echo "[INFO] Start of write_checkmate_params.sh"
if [ $# -ne 9 ]; then
	echo "$# params detected;\n"
	echo "[NAME] [ANALYSES] [SLHA] [QUIET MODE] [SEED] [OUTDIR] [NEV] [PROCESS] [CARD_DIR]"
	exit 1
fi
WDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
CARD_WRITER="${WDIR}/checkmate_params.py"

NAME=$1
ANALYSES=$2
SLHA=$(absolute_path $3) 
if [[ ! -e "${SLHA}" ]]; then
    echo "[ERROR] Input file not existing: ${SLHA}" 1>&2;
    exit 1
fi
QUIET=$4
SEED=$5
OUTDIR=$(absolute_path $6)
if [[ ! -d "$OUTDIR" ]]; then
	echo "[ERROR] Directory not existing: ${OUTDIR}" 1>&2;
	exit 1
fi
NEV=$7
# FOR FUTURE USE
XSECT='-1'
XSECTERR='-1'
#
PROCESS=$8
CARD_DIR=$(absolute_path $9)
if [[ ! -d "$CARD_DIR" ]]; then
	mkdir $CARD_DIR
	if [[ ! -d "$CARD_DIR" ]]; then
		echo "[ERROR] Directory not existing: ${CARD_DIR}" 1>&2;
		exit 1
	fi
fi
echo "[INFO] Writing params to ${CARD_DIR}/${NAME}.dat"

python ${CARD_WRITER} ${NAME} "${ANALYSES}" ${SLHA} ${QUIET} ${SEED} ${OUTDIR} ${NEV} ${XSECT} ${XSECTERR} "${PROCESS}" > ${CARD_DIR}"/${NAME}.dat" 
if [ $? -ne 0 ]; then
	echo "[ERROR] Could not create CheckMATE param card!"
	exit 1
fi
echo "[INFO] End of write_checkmate_params.sh"
