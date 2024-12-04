import numpy as np
from itertools import product
import matplotlib.pyplot as plt

with open("input.txt") as f:
    data = f.read().strip().split()

data = np.array(list(map(list, data)))
h, w = data.shape


# Q1
Xs = (data == "X").nonzero()
result = 0
result_array = np.zeros(data.shape)
for i, j in zip(*Xs):
    for k, m in product([-1, 0, 1], [-1, 0, 1]):
        if i + 3 * k < 0 or j + 3 * m < 0:
            continue
        try:
            word = data[i + k * np.arange(4), j + m * np.arange(4)]
            if "".join(word) == "XMAS":
                result += 1
                result_array[i + k * np.arange(4), j + m * np.arange(4)] += 1
        except IndexError:
            pass

print(result)
plt.imshow(result_array)
plt.show()

As = (data == "A").nonzero()
result = 0
result_array = np.zeros(data.shape)
for i, j in zip(*As):
    if i == 0 or j == 0 or i == h - 1 or j == w - 1:
        continue
    word1 = data[i - 1 + np.arange(3), j - 1 + np.arange(3)]
    word2 = data[i - 1 + np.arange(3), j + 1 - np.arange(3)]
    if set(word1) == set("MAS") and set(word2) == set("MAS"):
        result += 1
        result_array[i - 1 + np.arange(3), j - 1 + np.arange(3)] += 1
        result_array[i - 1 + np.arange(3), j + 1 - np.arange(3)] += 1

print(result)
plt.imshow(result_array)
plt.show()
