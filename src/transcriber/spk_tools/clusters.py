import json
from sklearn.cluster import KMeans
import numpy as np
import os


def get_central_vectors(v_list, num_speakers):
    kmeans = KMeans(init="random",
                    n_clusters=num_speakers,
                    n_init=10,
                    max_iter=300)

    # remove all 0-length vectors
    filtered_list = [i for i in v_list if len(i) == 128]
    kmeans.fit(np.array(filtered_list))

    # create central clusters and write them into a dictionary, keys are upcounting numbers
    central_vectors = kmeans.cluster_centers_
    central_vectors_dict = {str(i): central_vectors[i] for i in range(len(central_vectors))}

    # convert arrays back to lists
    for i in central_vectors_dict:
        central_vectors_dict[i] = list(central_vectors_dict[i])

    return central_vectors_dict
