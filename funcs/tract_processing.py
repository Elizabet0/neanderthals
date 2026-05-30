from collections import defaultdict
import pandas as pd
from funcs.merging import merge
from funcs.tract_extraction import get_population_tracts_dataframe

def get_tracts_dict(ts, n_eu, migration_times):
    tracts = defaultdict(list)
    for mig_time in migration_times:
        df = get_population_tracts_dataframe(ts, "EU", "ND", mig_time)
        for _, row in df.iterrows():
            ind = int(row['Sample'].split('_')[1])
            tracts[ind].append((row['Start'], row['End']))
    for i in range(n_eu):
        tracts[i] = merge(tracts[i])
    return tracts