#!/bin/bash
#SBATCH --output=$A_submit.out

for (( c=10; c<501; c++ ))
do
	A=$c
	b=10000
        sbatch --time=10:00  --account=def-mlaval --job-name=p_values_$A.$b.run --output=output/p_values/$A.$b.%j.out submit_p_values_script.sh $c 
done
