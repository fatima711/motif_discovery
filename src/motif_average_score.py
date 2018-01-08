import itertools
import pickle
import re
import pandas
import numpy
import math
import sys

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

alphabet = ["a","c", "g", "t", "[ag]", "[ct]", "."]
n = 8
allMotifs = list(itertools.product(alphabet,repeat=n)) #generates allmotifs of length n

# num_jobs = 10000
num_jobs = int(sys.argv[1])

# job_number = 10
job_number = int(sys.argv[2])

min_subgraph_size = 2
max_subgraph_size = 500

parts = list(chunks(allMotifs, round(len(allMotifs)/num_jobs)))
# print(len(parts))
if(job_number > len(parts)):
    quit()
motifs_for_this_job = parts[job_number]
# len(motifs_for_this_job)

protein_to_sequence = pickle.load( open( "../files/intermediates/proteins_to_sequences.pkl", "rb" ) )
protein_to_shuffled_sequence = pickle.load( open( "../files/intermediates/proteins_to_shuffled_sequences.pkl", "rb" ) )
distanceMatrix_df = pandas.read_pickle(open( "../files/intermediates/distanceMatrix.pkl", "rb" ))


# associating motifs to proteins

motifs_to_proteins = {}
motifs_to_proteins_shuffled = {}
for motif in motifs_for_this_job:
    motif = "".join(motif) #turning motif array into string
    motifs_to_proteins[motif] = []
    motifs_to_proteins_shuffled[motif] = []
    print(motif)
    for protein in protein_to_sequence:
#         if(motif in protein_to_sequence[protein]):
        if(re.search(motif, protein_to_sequence[protein]) != None):
            motifs_to_proteins[motif].append(protein)
            
    for protein in protein_to_shuffled_sequence:
#         if(motif in protein_to_sequence[protein]):
        if(re.search(motif, protein_to_shuffled_sequence[protein]) != None):
            motifs_to_proteins_shuffled[motif].append(protein)

# original dataset
motif_to_size = {}
motifs_to_average_scores = {}
motifs_to_tt_average_scores = {}
for motif in motifs_to_proteins:
    motif_to_size[motif] = len(motifs_to_proteins[motif])
#     making subgraph
    if( len(motifs_to_proteins[motif]) < min_subgraph_size or  len(motifs_to_proteins[motif]) > max_subgraph_size):
        continue
    proteins = motifs_to_proteins[motif]
    subgraph = [];
    for protein_i in proteins:
        row = []
        for protein_j in proteins:
            row.append(distanceMatrix_df[protein_i][protein_j])
        subgraph.append(row)
#     scoring
    avg_score = pandas.DataFrame(subgraph).mean().mean()
    ninety_p = numpy.percentile(subgraph, 90)
    for i, row in enumerate(subgraph):
        for j, elem in enumerate(row):
            if(elem < math.floor(ninety_p)):
                subgraph[i][j] = None
    tt_avg_score = pandas.DataFrame(subgraph).mean().mean()
    
    motifs_to_average_scores[motif] = avg_score
    motifs_to_tt_average_scores[motif] = tt_avg_score

# shuffled dataset
shuffled_motif_to_size = {}
shuffled_motifs_to_average_scores = {}
shuffled_motifs_to_tt_average_scores = {}
for motif in motifs_to_proteins_shuffled:
    shuffled_motif_to_size[motif] = len(motifs_to_proteins_shuffled[motif]) 
# preparing subgraph
    if( len(motifs_to_proteins_shuffled[motif]) < min_subgraph_size or  len(motifs_to_proteins_shuffled[motif]) > max_subgraph_size):
        continue
    proteins_shuffled = motifs_to_proteins_shuffled[motif]
    shuffled_subgraph = [];
    for protein_shuffled_i in proteins_shuffled:#shuffled subgraph
        row_shuffled = []
        for protein_shuffled_j in proteins_shuffled:
#             if(protein_shuffled_i != protein_shuffled_j):
            row_shuffled.append(distanceMatrix_df[protein_shuffled_i][protein_shuffled_j])
        shuffled_subgraph.append(row_shuffled)

    shuffled_avg_score = pandas.DataFrame(shuffled_subgraph).mean().mean()
    ninety_p_shuffled = numpy.percentile(shuffled_subgraph, 90)
    for i, row in enumerate(shuffled_subgraph):
        for j, elem in enumerate(row):
            if(elem < math.floor(ninety_p_shuffled)):
                shuffled_subgraph[i][j] = None
    tt_shuffled_avg_score = pandas.DataFrame(shuffled_subgraph).mean().mean()
    
    shuffled_motifs_to_average_scores[motif] = shuffled_avg_score
    shuffled_motifs_to_tt_average_scores[motif] = tt_shuffled_avg_score


# saving all data for job 
df = pandas.DataFrame({"motif_subgraph_size" : motif_to_size, "average_scores":motifs_to_average_scores, "average_tt_scores" : motifs_to_tt_average_scores,
                      "motif_shuffled_subgraph_size" : shuffled_motif_to_size, "shuffled_average_scores" : shuffled_motifs_to_average_scores, "shuffled_average_tt_scores" : shuffled_motifs_to_tt_average_scores})


df.to_pickle("../files/motif_scores/numJobs:" + str(num_jobs) + "_jobNumber:" + str(job_number) + ".pkl")
