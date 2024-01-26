import numpy as np
from itertools import combinations

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

map_dict = {".": 0, "#": 1}
input_data = np.array(
    [list(map(lambda x: map_dict[x], [*line])) for line in input_data]
)
# Q1
# mul_value = 2
# Q2
mul_value = 1_000_000
rows_to_expand = input_data.sum(axis=1) == 0
row_shift = (mul_value - 1) * rows_to_expand.cumsum()
cols_to_expand = input_data.sum(axis=0) == 0
col_shift = (mul_value - 1) * cols_to_expand.cumsum()

pairs = combinations(zip(*np.where(input_data == 1)), 2)

distances = 0
for (i, j), (k, l) in pairs:
    distances += abs(i + row_shift[i] - k - row_shift[k]) + abs(
        j + col_shift[j] - l - col_shift[l]
    )

print(distances)
