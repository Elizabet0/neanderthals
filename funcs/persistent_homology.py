def persistence_summary(dm):
    r=Rips(maxdim=1)
    d=r.fit_transform(dm, distance_matrix=True)
    h0=d[0]
    h1=d[1]

    if len(h0)>0:
        fin=h0[:,1]!=np.inf
        p0=h0[:,1]-h0[:,0]
        H0_total=np.sum(p0[fin])
        H0_max=np.max(p0[fin]) if np.any(fin) else 0
    else:
        H0_total=0
        H0_max=0

    if len(h1)>0:
        p1=h1[:,1]-h1[:,0]
        H1_total=np.sum(p1)
        H1_max=np.max(p1)
        H1_n=len(h1)
    else:
        H1_total=0
        H1_max=0
        H1_n=0

    return {'H0_total_persistence':H0_total, 'H0_max_persistence':H0_max, 
            'H1_total_persistence':H1_total, 'H1_max_persistence':H1_max, 'H1_number_of_features':H1_n} 