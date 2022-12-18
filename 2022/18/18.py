import pandas as pd
import numpy as np

input_data = pd.read_csv("input.txt", header=None)

def get_faces(cubes_coords):
    faces = 0
    for dimension in range(3):
        for _, column in cubes_coords.groupby([i for i in range(3) if i != dimension]):
            column = column[dimension].sort_values()
            faces += 2 + 2 * (column.diff() > 1).sum()
    return faces
faces = get_faces(input_data)
print(faces)

h, w, d = input_data.max()
volume = np.zeros((h + 1, w + 1, d + 1))
for _, (i, j, k) in input_data.iterrows():
    volume[i, j, k] = 1


def dfs(i, j, k):
    positions = [
        [i + 1, j, k],
        [i - 1, j, k],
        [i, j - 1, k],
        [i, j + 1, k],
        [i, j, k - 1],
        [i, j, k + 1],
    ]
    for i1, j1, k1 in positions:
        if i1 < 0 or j1 < 0 or k1 < 0:
            continue
        if i1 > h or j1 > w or k1 > d:
            continue
        if volume[i1, j1, k1] == 0:
            volume[i1, j1, k1] = 2
            dfs(i1, j1, k1)

import sys
sys.setrecursionlimit(volume.size)
dfs(0, 0, 0)
negative_cubes = pd.DataFrame((volume == 0).nonzero()).T
negative_faces = get_faces(negative_cubes)

print(faces - negative_faces)