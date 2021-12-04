import numpy as np
import pandas as pd

with open("input.txt") as f:
    draws = [int(n) for n in f.readline().split(",")]
    grids = f.readlines()

grid_list = []
grid = []
for row in grids[1:]:
    if row == "\n":
        grid_list.append(grid)
        grid = []
    else:
        grid_line = [int(n) for n in row[:-1].split(" ") if n]
        grid.append(grid_line)
grids = np.array(grid_list)
ngrids = len(grid_list)
found = grid != grid

for d in draws:
    found = found | (grids == d)
    won = np.argwhere((found.all(axis=1) | found.all(axis=2)).any(axis=1))[:, 0]
    if len(won) > 0:
        win_index = won[0]
        score = (grids[win_index] * ~found[win_index]).sum()
        print(score * d)
        break

last_win_index = -1
for d in draws:
    found = found | (grids == d)
    won = np.argwhere((found.all(axis=1) | found.all(axis=2)).any(axis=1))
    if last_win_index == -1:
        if len(won) == ngrids - 1:
            last_win_index = (set(range(ngrids)) - set(won[:, 0])).pop()
    elif len(won) == ngrids:
        score = (grids[last_win_index] * ~found[last_win_index]).sum()
        print(score * d)
        break
        