#!/bin/bash
#SBATCH --output=$A_submit.out

for (( c=761; c<=761; c++ ))
do
	a=1000
	b=$c
	sbatch --time=175:00 --mem-per-cpu=8120 --account=def-mlaval --job-name=output/motif/job/$a.$b.run --output=output/motif/$a.$b.%j.out submit_motif_script.sh $a $b 
done