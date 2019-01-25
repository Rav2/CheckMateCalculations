FILE_PATH="/RESULTS/primary/QqN1/lists"
FILE_NAME="QqN1_atlas_1712_02332"

NO_START=0
NO_END=2
STEP=1

for (( IT = $NO_START; IT <= $NO_END; IT += $STEP ))
	do
		ARG=$FILE_PATH"/"$FILE_NAME"_["$IT"].txt"
		qsub -N $FILE_NAME"_["$IT"]" -v arg=$ARG /home/2/rm394969/udocker-1.1.3/usetting.sh
	done


