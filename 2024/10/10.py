import numpy as np
from itertools import product
from tqdm import tqdm

with open("input.txt") as f:
    input_data = f.read().strip().split()

input_data = np.array(list(map(list, input_data)), dtype=int)
h, w = input_data.shape

start_points = (input_data == 0).nonzero()


def next_step(
    position: tuple[int, int],
    nine_set: set[tuple[int, int]],
    nine_list: list[tuple[int, int]],
):
    if input_data[*position] == 9:
        nine_set.add(position)
        nine_list.append(position)

    for i, j in product([-1, 0, 1], [-1, 0, 1]):
        if i * j != 0:
            continue
        next_position = (position[0] + i, position[1] + j)
        if (
            next_position[0] < 0
            or next_position[1] < 0
            or next_position[0] == h
            or next_position[1] == w
        ):
            continue
        if input_data[*next_position] == input_data[*position] + 1:
            next_step(next_position, nine_set, nine_list)


result1 = 0
result2 = 0
for i, j in tqdm(zip(*start_points), total=len(start_points[0])):
    nine_set = set()
    nine_list = []
    next_step((i, j), nine_set, nine_list)
    result1 += len(nine_set)
    result2 += len(nine_list)

print(result1)
print(result2)
