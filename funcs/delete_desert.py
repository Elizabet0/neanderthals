from funcs.merging import merge

def remove_desert_from_tracts(tracts,desert_start, desert_end):
    new_tracts={}
    for ind,segs in tracts.items():
        updated=[]
        for s,e in segs:
            if e<=desert_start or s>=desert_end:
                updated.append((s,e))
            else:
                if s<desert_start: 
                    updated.append((s,desert_start))
                if e>desert_end:
                    updated.append((desert_end,e))
        new_tracts[ind]=merge(updated)
    return new_tracts