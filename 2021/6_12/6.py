import pandas as pd

fishes = pd.read_csv("input.txt", header=None, dtype=int).T
fishes = fishes.groupby(0).size().reindex(range(9)).fillna(0).astype(int)

ndays = 256
for i in range(ndays):
    fishes.index -=1
    new_fishes = fishes.reindex(range(9)).fillna(0).astype(int)
    new_fishes[8] = fishes[-1]
    new_fishes[6] += fishes[-1]
    fishes = new_fishes
print(fishes.sum())