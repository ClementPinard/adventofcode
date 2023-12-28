from collections import defaultdict
import numpy as np
from sklearn.cluster import SpectralClustering

input_data = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

graph = defaultdict(set)
for line in input_data:
    src, dest = line.split(": ")
    dest = dest.split(" ")
    graph[src] = graph[src] | set(dest)
    for d in dest:
        graph[d].add(src)

keys = {k: i for i, k in enumerate(graph.keys())}
matrix = np.zeros((len(keys), len(keys)))

for node, dest in graph.items():
    for d in dest:
        matrix[keys[node], keys[d]] = 1

a = SpectralClustering(n_clusters=2, affinity="precomputed")
labels = a.fit_predict(matrix)
print((labels == 1).sum() * (labels == 0).sum())
