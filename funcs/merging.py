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