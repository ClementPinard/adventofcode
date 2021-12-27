from scipy.signal import convolve2d
import numpy as np

with open("input.txt") as f:
    algo, image = f.read().split("\n\n")

algo = [0 if c=='.' else 1 for c in algo]
algo = np.array(list(algo), dtype=int)
image = [[0 if c=='.' else 1 for c in line] for line in image.splitlines()]
image = np.array(image, dtype=int)

surrounding = 0
index_array = np.power(2, np.arange(9)).reshape((3,3))
print(index_array)

for i in range(50):
    indexed = convolve2d(image, index_array, fillvalue=surrounding)
    surrounding = algo[(index_array * surrounding).sum()]
    image = algo[indexed]
    print(image.sum())