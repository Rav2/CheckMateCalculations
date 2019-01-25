# !/bin/bash

INPUT="./grid/minigrid.dat"
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
	line_no=0
	while IFS= read -r LINE<&4 || [[ -n "$LINE" ]]; do
		LINE="$(echo -e "${LINE}" | sed -e 's/[[:space:]]*$//')"
		if [[ !( "$LINE" =~ ^#.*$ ) ]]; then
			echo $LINE

		fi
	done
	exec 4<&-
fi