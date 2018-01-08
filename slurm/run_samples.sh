#!/bin/bash
#SBATCH --output=$A_submit.out

for (( c=237; c<250; c++ ))
do
	A=$c
	b=10000
        sbatch --time=270:00 --mem-per-cpu=8192 --account=def-mlaval --job-name=output/samples/job/$A.$b.run --output=output/samples/$A.$b.%j.out submit_samples_script.sh $c 
done
