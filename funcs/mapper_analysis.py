def mapper_summary(graph):
    g=to_networkx(graph)
    n=g.number_of_nodes()
    e=g.number_of_edges()

    comps=list(nx.connected_components(g))
    nc=len(comps)
    diam=0

    for comp in comps:
        sg=g.subgraph(comp)
        if len(comp)>1:
            try:
                diam=max(diam,nx.diameter(sg))
            except:
                pass

    branch=sum(g.degree(node)>2 for node in g.nodes())
    cyc=e-n+nc if n>0 else 0
    return {'nodes':n, 'edges':e, 'components':nc, 
            'diameter':diam, 'branch_nodes':branch, 'cycles':cyc}