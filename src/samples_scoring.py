import pandas
import pickle
import numpy as np
import sys

size = int(sys.argv[1])

protein_to_sequence = pickle.load( open( "../files/intermediates/proteins_to_sequences.pkl", "rb" ) )
distanceMatrix_df = pandas.read_pickle(open( "../files/intermediates/distanceMatrix.pkl", "rb" ))

# size = 100
proteins = list(protein_to_sequence.keys())
probability_frequency = [len(sequence) for sequence in protein_to_sequence.values()]
probability_distribution = [freq/sum(probability_frequency) for freq in probability_frequency]


number_of_samples_needed = 10000
samples_scores = {"average_scores" : [], "tt_average_scores" :[]}

for i in range(0, number_of_samples_needed):
    sample = np.random.choice(proteins, size, p = probability_distribution, replace = False)
    sample_subgraph = []
    for protein_i in sample:#original subgraph
        row = []
        for protein_j in sample:
            if(protein_i != protein_j):
                row.append(distanceMatrix_df[protein_i][protein_j])
        sample_subgraph.append(row)
    avg_score = pandas.DataFrame(sample_subgraph).mean().mean()
    ninety_p_shuffled = np.percentile(sample_subgraph, 90)
    for i, row in enumerate(sample_subgraph):
        for j, elem in enumerate(row):
            if(elem < ninety_p_shuffled):
                sample_subgraph[i][j] = None
                
    tt_avg_score = pandas.DataFrame(sample_subgraph).mean().mean()
#     print(avg_score, tt_avg_score)
    samples_scores["average_scores"].append(avg_score)
    samples_scores["tt_average_scores"].append(tt_avg_score)
pickle.dump( samples_scores,open( "../files/intermediates/samples/sample_" + str(size) + ".pkl", "wb" ) )