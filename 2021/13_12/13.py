import numpy as np

with open("input.txt") as f:
    data1, data2 = f.read().split('\n\n')
    print(data1)
data = np.array([d.split(',') for d in data1.splitlines()], dtype=int)
points = np.zeros(data.max(axis=0)+1, dtype=int)
points[data[:,0], data[:,1]] = 1

def fold_along(points, axis, coord):
    if axis == "y":
        points = points.T
    fold_size = points.shape[0] - coord - 1
    output_points = points[:coord]
    output_points[-fold_size:] += points[coord+1:][::-1]
    if axis == "y":
        output_points = output_points.T
    return (output_points > 0).astype(int)

print(points)
folds = [d.split("=") for d in data2.splitlines()]
print(folds)
for axis, coord in folds:
    points = fold_along(points, axis[-1], int(coord))
    print((points > 0).sum())

import matplotlib.pyplot as plt
plt.imshow(points.T)
plt.show()