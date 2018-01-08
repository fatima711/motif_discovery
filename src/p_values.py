import pickle
import pandas
import numpy as np
import math
import sys


size = sys.argv[1]


motifs_of_size =  pickle.load(open( "../files/intermediates/motifs_to_size/motifs_of_size" + str(size) + ".pkl", "rb" ))
motifs_of_size_shuffled =   pickle.load( open( "../files/intermediates/motifs_to_size/shuffled_motifs_of_size" + str(size) + ".pkl", "rb" ) )


samples =  pickle.load( open( "../files/intermediates/samples/sample_" + str(size) + ".pkl", "rb" ) )
average_sample_scores_of_size = np.array(samples['average_scores'])
tt_average_sample_scores_of_size = np.array(samples['tt_average_scores'])
total_distribution = len(samples['average_scores'])


motifs_to_p_values = {}
motifs_to_tt_p_values = {}

for motif_t in motifs_of_size:
    motif = motif_t[0]
    motif_average_score = motif_t[1]
    motif_tt_average_score = motif_t[2]
    right_of_distribution = sum(average_sample_scores_of_size > motif_average_score)
    tt_right_of_distribution = sum(tt_average_sample_scores_of_size > motif_tt_average_score)
    if(math.isnan(motif_average_score)):
        p_value = float('nan')
        tt_p_value = float('nan')
    else:
        p_value = right_of_distribution/total_distribution
        tt_p_value = tt_right_of_distribution/total_distribution 
    
    motifs_to_p_values[motif] = p_value
    motifs_to_tt_p_values[motif] = tt_p_value
 

motifs_to_shuffled_p_values = {}
motifs_to_shuffled_tt_p_values = {}

for motif_shuffled_t in motifs_of_size_shuffled:
    motif = motif_shuffled_t[0]
    motif_shuffled_average_score = motif_shuffled_t[1]
    motif_tt_shuffled_average_score = motif_shuffled_t[2]
    right_of_distribution = sum(average_sample_scores_of_size > motif_shuffled_average_score)
    tt_right_of_distribution = sum(tt_average_sample_scores_of_size > motif_tt_shuffled_average_score)
    
    if(math.isnan(motif_shuffled_average_score)):
        shuffled_p_value = float('nan')
        tt_shuffled_p_value = float('nan')
    else:
        shuffled_p_value = right_of_distribution/total_distribution
        tt_shuffled_p_value = tt_right_of_distribution/total_distribution

    motifs_to_shuffled_p_values[motif] = shuffled_p_value
    motifs_to_shuffled_tt_p_values[motif] = tt_shuffled_p_value

df = pandas.DataFrame({
                "motif_p_value" : motifs_to_p_values, "motif_tt_p_value":motifs_to_tt_p_values,
                "motif_shuffled_p_value" : motifs_to_shuffled_p_values, "motif_shuffled_tt_p_value" : motifs_to_shuffled_tt_p_values, 
                  })

df.to_pickle("../files/intermediates/p_values/p_values_for_motifs_of_size_" +str(size) + ".pkl")

