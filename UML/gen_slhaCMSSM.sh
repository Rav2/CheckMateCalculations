# !/bin/bash

PREFIX="cmssm"
INPUT="./grid/gridCMSSM.dat"
WRITE_SLHA="./write_slhaCMSSM.py"
RESULT_PATH="./SLHA"

if [[ ! -d "$RESULT_PATH" ]]; then
	mkdir $RESULT_PATH
	if [[ ! -e "$RESULT_PATH" || ! -d "$RESULT_PATH" ]]; then
		echo "[ERROR] Could not create directory for data!"
		exit 1
	fi
fi

if [[ -e $WRITE_SLHA ]]; then
	echo "[INFO] Generating SLHA files!"
	exec 4< $INPUT
	line_no=1
	while IFS= read -r LINE<&4 || [[ -n "$LINE" ]]; do
		# echo "[INFO] LINE: $line_no"
		LINE="$(echo -e "${LINE}" | sed -e 's/[[:space:]]*$//')"
		if [[ !( "$LINE" =~ ^#.*$ ) ]]; then
			NAME="$PREFIX" 
			for STR in $LINE; do
				NAME=$NAME"_"$STR
			done
			# prevent susyhit NaN behavior when mG or mQ is equal to one of the other masses
			ARRNAME=(${NAME//_/ })
			# check for m0 and m1/2
			if [[ ${ARRNAME[1]} == ${ARRNAME[2]} ]]; then
				m=$(( ${ARRNAME[1]} - 1 ))
				LINE=${LINE/${ARRNAME[1]}/${m}}
			fi
			# name is not changed but slha yes
			NAME=$NAME".slha"
			python3 $WRITE_SLHA $LINE > $NAME
			mv $NAME $RESULT_PATH
			# echo ${NAME}
		fi
	line_no=$(( $line_no + 1))
	done
	exec 4<&-
fi
