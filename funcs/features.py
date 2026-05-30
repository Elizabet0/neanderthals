import numpy as np 

def build_binary_matrix(tracts,n, w_size, M):
    X = np.zeros((n,M),dtype=int)
    for ind,segs in tracts.items():
        for s,e in segs:
            l=max(0,int(np.floor(s/w_size)))
            r=min(M,int(np.ceil(e/w_size)))
            X[ind,l:r]=1
    return X
