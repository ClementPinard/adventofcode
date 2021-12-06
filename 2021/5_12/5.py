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
        x_step = np.sign(x2 - x1)
        y_step = np.sign(y2 - y1)
        visited[range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)] += 1
        visited[x2, y2] += 1

import matplotlib.pyplot as plt

plt.imshow(visited)
plt.colorbar()
plt.show()
print((visited >= 2).sum())
        
