import pandas as pd
import numpy as np
from scipy.ndimage import binary_fill_holes

input_data = pd.read_csv("input.txt", header=None)


def get_faces(cubes_coords):
    faces = 0
    for dimension in range(3):
        for _, column in cubes_coords.groupby([i for i in range(3) if i != dimension]):
            column = column[dimension].sort_values()
            faces += 2 + 2 * (column.diff() > 1).sum()
    return faces


faces = get_faces(input_data)
# Q1
print(faces)

h, w, d = input_data.max()
volume = np.zeros((h + 1, w + 1, d + 1))
for _, (i, j, k) in input_data.iterrows():
    volume[i, j, k] = 1

volume = binary_fill_holes(volume)
filled_cubes = pd.DataFrame((volume).nonzero()).T
faces = get_faces(filled_cubes)

# Q2
print(faces)
