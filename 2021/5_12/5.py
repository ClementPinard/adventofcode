import numpy as np
from collections import defaultdict

with open("input.txt") as f:
    rows = [[r.split(",") for r in r1] for r1 in [r2[:-1].split(" -> ") for r2 in f.readlines()]]
    rows = np.array(rows, dtype=int)

maxx, maxy = rows.max(axis=0).max(axis=0)
visited = np.zeros((maxx+1, maxy+1))
for r in rows:
    (x1, y1), (x2, y2) = r
    xmin, ymin = r.min(axis=0)
    xmax, ymax = r.max(axis=0)
    if (xmax == xmin) or (ymax == ymin):
        visited[xmin:xmax+1, ymin:ymax+1] += 1
    else:
        assert((xmax - xmin) == (ymax - ymin))
        visited[range(x1, x2, np.sign(x2 - x1)), range(y1, y2, np.sign(y2 - y1))] += 1
        visited[x2, y2] += 1
print((visited >= 2).sum())
        
