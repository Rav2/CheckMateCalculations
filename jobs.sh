FILE_PATH="/RESULTS/primary/GqqN1/lists"
FILE_NAME="GqqN1_atlas_1712_02332"

NO_START=0
NO_END=399
STEP=1

for (( IT = $NO_START; IT <= $NO_END; IT += $STEP ))
	do
                NODE=$(( $IT % 10 + 11 ))
		ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
		qsub -N $FILE_NAME"_["$IT"]" -l nodes="w"$NODE -v arg=$ARG /home/2/rm394969/udocker-1.1.3/usetting.sh
	done


