import numpy as np

with open("input.txt") as f:
    heightmap = [list(r[:-1]) for r in f.readlines()]

heightmap = np.array(heightmap, dtype=int)

local_minima = np.full_like(heightmap, fill_value=True, dtype=bool)
h_grad = (heightmap[:-1] - heightmap[1:])
v_grad = (heightmap[:,:-1] - heightmap[:, 1:])
local_minima[:-1] *= (h_grad < 0)
local_minima[1:] *= (h_grad > 0)
local_minima[:, :-1] *= (v_grad < 0)
local_minima[:, 1:] *= (v_grad > 0)

print((heightmap[local_minima] + 1).sum())

def find_next_in_bassin(i,j):
    bassin = {(i,j)}
    for i1 in range(i-1, i+2):
        for j1 in range(j-1, j+2):
            if (i1 < 0) or (j1 < 0) or (i1 >= heightmap.shape[0]) or (j1 >= heightmap.shape[1]) or (heightmap[i1, j1] == 9):
                continue
            if heightmap[i1, j1] > heightmap[i,j]:
                bassin |= {(i1, j1)}
                bassin |= find_next_in_bassin(i1, j1)
    return bassin

bassins = []
for lmi, lmj in  zip(*local_minima.nonzero()):
    bassins.append(find_next_in_bassin(lmi,lmj))

bassin_sizes = sorted([len(bassin) for bassin in bassins])
print(bassin_sizes[-3] * bassin_sizes[-2] * bassin_sizes[-1])
