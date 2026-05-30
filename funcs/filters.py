import numpy as np
from sklearn.manifold import MDS
import pandas as pd

def compute_filter(filter_name, X, dist, bio_df):
    if filter_name=="MDS1":
        mds=MDS(n_components=1,dissimilarity='precomputed',
                      random_state=0,normalized_stress='auto')
        try:
            return mds.fit_transform(dist)
        except:
            return np.zeros((dist.shape[0],1))
    elif filter_name=="distance_to_medoid":
        medoid=np.argmin(dist.mean(axis=0))
        return dist[:,medoid].reshape(-1,1)
    elif filter_name=="mean_distance":
        return dist.mean(axis=1).reshape(-1,1)
    elif filter_name=="introgressed_fraction":
        return bio_df[['introgressed_fraction']].values
    elif filter_name=="tract_count":
        return bio_df[['tract_count']].values
    elif filter_name=="mean_tract_length":
        return bio_df[['mean_tract_length']].values
