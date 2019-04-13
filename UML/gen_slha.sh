# !/bin/bash

PREFIX="grid"
INPUT="./grid/grid.dat"
WRITE_SLHA="./write_slha.py"
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
			# check for mG
			if [[ ${ARRNAME[1]} == ${ARRNAME[2]} || ${ARRNAME[1]} == ${ARRNAME[3]} || ${ARRNAME[1]} == ${ARRNAME[4]} ]]; then
				mG=$(( ${ARRNAME[1]} - 1 ))
				LINE=${LINE/${ARRNAME[1]}/${mG}}
			fi
			# name is not changed but slha yes
			NAME=$NAME".slha"
			python $WRITE_SLHA $LINE > $NAME
			mv $NAME $RESULT_PATH
			# echo ${NAME}
		fi
	line_no=$(( $line_no + 1))
	done
	exec 4<&-
fi
