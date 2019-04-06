#!/bin/bash

START=1
END=3394
STEP=10

tmux start-server
for ((ii=${START}; ii<${END}; ii+=${STEP}))
	do
		#if [[ $ii == $START ]]; then
		#	continue
		#fi 
		NEXT=$(( ${ii} + ${STEP} ))
		if [[ ${NEXT} -gt $END ]]; then
			NEXT=$END
		fi
		tmux new-session -d -s "session_$ii"
		tmux send-keys -t "session_$ii:0" "cd /home/2/rm394969/udocker-1.1.3/ ; ./skrypt.sh " Enter 
		tmux send-keys -t "session_$ii:0" "/CheckMATECalculations/udocker_scripts/jobs_tmux.sh $ii $NEXT " Enter

		#tmux detach -s "session_$ii"
	done

