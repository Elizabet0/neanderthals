import numpy as np
import pandas as pd
import tskit
from collections import defaultdict

def get_migrating_tracts_ind(ts,pop_name,ind_node,T_anc):
    pop_id=-1
    for p in ts.populations():
        if p.metadata.get('name')==pop_name:
            pop_id=p.id
            break
    if pop_id==-1:
        return []
    tables=ts.tables
    mask=((tables.migrations.time==T_anc)&(tables.migrations.dest==pop_id))
    relevant=np.where(mask)[0]
    mig_lookup={}
    for i in relevant:
        node=tables.migrations.node[i]
        interval=(tables.migrations.left[i],tables.migrations.right[i])
        mig_lookup.setdefault(node,[]).append(interval)
    tracts=[]
    for tree in ts.trees():
        anc=ind_node
        if ts.node(anc).time>T_anc:
            continue
        parent=tree.parent(anc)
        while (parent!=tskit.NULL and ts.node(parent).time<=T_anc):
            anc=parent
            parent=tree.parent(anc)
        if anc in mig_lookup:
            t_l,t_r=tree.interval
            for m_l,m_r in mig_lookup[anc]:
                s=max(t_l,m_l)
                e=min(t_r,m_r)
                if s<e:
                    if tracts and tracts[-1][1]==s:
                        tracts[-1][1]=e
                    else:
                        tracts.append([s,e])
    return tracts

def get_population_tracts_dataframe(ts, target_pop, source_pop, migration_time):
    t_id=-1
    for p in ts.populations():
        if p.metadata.get('name')==target_pop:
            t_id=p.id
            break
    nodes=ts.samples(population=t_id)
    if len(nodes)==0:
        return pd.DataFrame(columns=["Sample","Start","End","Length"])
    ind_ids=np.unique(ts.nodes_individual[nodes])
    ind_ids=ind_ids[ind_ids!=-1]
    data=[]
    for ind in ind_ids:
        individual=ts.individual(ind)
        for i,node in enumerate(individual.nodes):
            sample_name=f"{target_pop}_{ind}_{i+1}"
            tracts=get_migrating_tracts_ind(
                ts,
                source_pop,
                node,
                migration_time
            )
            for s,e in tracts:
                data.append({
                    "Sample":sample_name,
                    "Start":int(s),
                    "End":int(e),
                    "Length":int(e-s)
                })
    return pd.DataFrame(data)

def merge(intervals):
    if not intervals:
        return []
    intervals.sort()
    res = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= res[-1][1]:
            res[-1] = (res[-1][0], max(res[-1][1], e))
        else:
            res.append((s, e))
    return res

def get_tracts_dict(ts, n_eu, migration_times):
    tracts=defaultdict(list)
    for mig_time in migration_times:
        df=get_population_tracts_dataframe(ts, "EU", "ND", mig_time)
        for _,row in df.iterrows():
            ind=int(row['Sample'].split('_')[1])
            tracts[ind].append((row['Start'], row['End']))
    for i in range(n_eu):
        tracts[i]=merge(tracts[i])
    return tracts