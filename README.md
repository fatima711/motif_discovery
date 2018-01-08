# motif_discovery

This repo is started after my honors project was complete. The initial project was written in Java, and did not have conclusive results due to a very high false discovery ratio.

I rewrote the entire analysis in python when I had more time.

1. It begins in with the preprocess_biological_network_inputs.ipynb file. 

2. After wards if you have access to a compute cluster using slurm. Run the run_samples and run_motifs files.

This will run in the scoring scripts located in the src directory in parallel. 

Because the scoring is an n^2 algorithm, I allocated the following times for the scoring of samples. 

sample sizes    time allocated in minutes
0-50            7.5
50-100          30.0
100-150         67.5
150-200         120.0
200-250         187.5
250-300         270.0
300-350         367.50000000000006
350-400         480.00000000000006
400-450         607.5000000000001
450-500         750.0000000000002
Total = 0.28 cpu/years

Motifs are seperated into 1000 jobs, and their upper bound in size. With those motifs the average subgraph size was 237 and 289 for the shuffled subgraphs. With about 5764 motifs being scored twice per file. I chose to allocated 187.5 minutes per job since it was sufficient for 10000 samples of size up to 250.

1000 jobs * 187.5 minutes per job = 0.36 cpu/years.

3. Run the p_value_preprocess.ipynb file

4. Again if you have access to a compute cluster you can run the run_p_value.sh file to run in parralel 1 job for each size. In this analysis we consider sizes 2 to 500. 10 minutes was more than suffiecient to run a single size on my local machine so I chose to allocate that much time on the cluster per job. This takes approximately 3.5 cpu/days to run.

5. Run post_process.ipynb to get all the results from the many files into database tables.

6. Run results to analyse the results in different plots and calculate the FDR for the different p-values and plot that.
