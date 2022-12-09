import pandas as pd
import numpy as np

input_data = pd.read_csv("input.txt", header=None, sep=" ")
directions = {"U": [1, 0], "D": [-1, 0], "L": [0, -1], "R": [0, 1]}
directions = {k: np.array(v) for k, v in directions.items()}


def update(h_pos, t_pos):
    diff = h_pos - t_pos
    if np.abs(diff).max() <= 1:
        return t_pos
    else:
        new_diff = np.sign(diff) * (np.abs(diff) == 2)
        return h_pos - new_diff


# Q1
# n_knots = 2
# Q2
n_knots = 10
positions = np.zeros((n_knots, 2), dtype=int)
visited = {}
for _, (d, magnitude) in input_data.iterrows():
    while magnitude > 0:
        positions[0] += directions[d]
        for i in range(1, n_knots):
            positions[i] = update(positions[i - 1], positions[i])
            visited[tuple(positions[i])] = max(i, visited.get(tuple(positions[i]), 0))
        magnitude -= 1

max_x = max(visited, key=lambda x: x[0])[0]
max_y = max(visited, key=lambda x: x[1])[1]
min_x = min(visited, key=lambda x: x[0])[0]
min_y = min(visited, key=lambda x: x[1])[1]
result = np.zeros((max_x - min_x + 1, max_y - min_y + 1))
for (x, y), i in visited.items():
    result[x - min_x, y - min_y] = i

result = result[::-1]

import matplotlib.pyplot as plt

plt.imshow(result)
plt.show()
print((result == n_knots - 1).sum())
