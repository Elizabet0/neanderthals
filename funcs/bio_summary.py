import numpy as np
import pandas as pd
import sys
sys.path.append('..')
from parameters import params 


def build_individual_biology(tracts, X, scenario):
    rows=[]
    for ind in range(params['n_eu']):
        segs=tracts[ind]
        introgressed_windows=int(X[ind].sum())
        introgressed_fraction=float(
            X[ind].mean()
        )
        tract_count=len(segs)
        if tract_count>0:
            mean_tract_length=np.mean([
                e-s for s,e in segs
            ])
        else:
            mean_tract_length=0
        rows.append({
            'scenario':scenario,
            'individual_id':ind,
            'introgressed_windows':introgressed_windows,
            'introgressed_fraction':introgressed_fraction,
            'tract_count':tract_count,
            'mean_tract_length':mean_tract_length
        })
    return pd.DataFrame(rows)