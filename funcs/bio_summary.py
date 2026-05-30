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