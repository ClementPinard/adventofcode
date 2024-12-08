import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from fractions import Fraction

with open("input.txt") as f:
    input_data = f.read().strip().split()

input_data = np.array(list(map(list, input_data)))
h, w = input_data.shape
antennas = {
    letter: np.stack((input_data == letter).nonzero()).T
    for letter in np.unique(input_data)
    if letter != "."
}


def in_bound(x, y):
    return x >= 0 and x < h and y >= 0 and y < w


# Q1
result_array = np.zeros(input_data.shape)
for letter, antennas_coords in antennas.items():
    for a1, a2 in combinations(antennas_coords, r=2):
        antinode1 = 2 * a1 - a2
        antinode2 = 2 * a2 - a1
        if in_bound(*antinode1):
            result_array[*antinode1] = 1
        if in_bound(*antinode2):
            result_array[*antinode2] = 1

plt.imshow(result_array)
plt.show()

print(result_array.sum())

# Q2

result_array = np.zeros(input_data.shape)
for letter, antennas_coords in antennas.items():
    for a1, a2 in combinations(antennas_coords, r=2):
        diff = Fraction(*(a2 - a1))
        smallest_diff = np.array([diff.numerator, diff.denominator])
        current_point = a1.copy()
        while in_bound(*current_point):
            result_array[*current_point] = 1
            current_point += smallest_diff
        current_point = a1.copy()
        while in_bound(*current_point):
            result_array[*current_point] = 1
            current_point -= smallest_diff

plt.imshow(result_array)
plt.show()
print(result_array.sum())
