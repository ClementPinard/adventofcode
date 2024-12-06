import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

with open("input.txt") as f:
    input_data = list(map(list, f.read().strip().split()))

input_data = np.array(input_data)
visited = np.zeros(input_data.shape)
obstacles = (input_data == "#").nonzero()
start_guard = (input_data == "^").nonzero()
start_guard = [start_guard[0][0], start_guard[1][0]]
visited[obstacles] = -1
visited[start_guard[0], start_guard[1]] = 1


def patrol(current_vis, start_guard):
    guard = start_guard
    possible_loop = -3
    while True:
        next_possible = (current_vis[: guard[0], guard[1]] == -1).nonzero()[0]
        if len(next_possible) == 0:
            current_vis[: guard[0] + 1, guard[1]] = 1
            return False
        next_possible = next_possible.max() + 1
        current_vis[next_possible + 1 : guard[0] + 1, guard[1]] = 1
        guard = [current_vis.shape[1] - guard[1] - 1, next_possible]
        current_vis = np.rot90(current_vis)
        if current_vis[guard[0], guard[1]] == 1:
            if possible_loop > 0:
                return True
            else:
                possible_loop += 1
        else:
            possible_loop = -3


# Q1
visisted1 = visited.copy()
is_loop = patrol(visisted1, start_guard)
print((visisted1 == 1).sum())


# Q2
result = 0
positions = (visisted1 == 1).nonzero()
for i, j in tqdm(zip(*positions), total=positions[0].shape[0]):
    if start_guard == [i, j]:
        continue
    start = visited.copy()
    start[i, j] = -1
    is_loop = patrol(start, start_guard)
    if is_loop:
        result += 1

print(result)
