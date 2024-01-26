from tqdm import trange
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from functools import cache

input_data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]


rocks = set()


def distance_map(start, rocks, h, w):
    distances = {start: 0}
    new_blocks = {start}
    while new_blocks:
        i, j = new_blocks.pop()
        for di, dj in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            new_position = (i + di, j + dj)
            if (
                new_position in rocks
                or new_position[0] < 0
                or new_position[1] < 0
                or new_position[0] >= h
                or new_position[1] >= w
            ):
                continue
            if (
                new_position in distances
                and distances[new_position] <= distances[(i, j)] + 1
            ):
                continue
            new_blocks.add(new_position)
            distances[new_position] = distances[(i, j)] + 1
    return distances


def possible_pos(distance_map, start_steps, n_steps):
    return (
        (distance_map >= 0)
        & (distance_map + start_steps <= n_steps)
        & (((distance_map + start_steps) % 2) == (n_steps % 2))
    ).sum()


h, w = len(input_data), len(input_data[0])

for i, line in enumerate(input_data):
    for j, c in enumerate(line):
        if c == "#":
            rocks.add((i, j))
        elif c == "S":
            start = (i, j)
n_steps = 64
distances = distance_map(start, rocks, h, w)
distances_np = np.full((h, w), -1)
for pos, value in distances.items():
    distances_np[pos] = value
print(possible_pos(distances_np, 0, n_steps))

# Q2
rocks_bis = set(
    (h * i + i_, w * j + j_)
    for (i, j) in product(range(3), range(3))
    for (i_, j_) in rocks
)
distances_bis = distance_map((h + start[0], w + start[1]), rocks_bis, 3 * h, 3 * w)
distances_bis_np = np.full((3 * h, 3 * w), -1)
for (i, j), v in distances_bis.items():
    distances_bis_np[i, j] = v


n_steps = 26501365
quarters = [
    distances_bis_np[h + start[0] : 2 * h + start[0], w + start[1] : 2 * w + start[1]],
    distances_bis_np[h + start[0] : start[0] : -1, w + start[1] : 2 * w + start[1]],
    distances_bis_np[h + start[0] : 2 * h + start[0], w + start[1] : start[1] : -1],
    distances_bis_np[h + start[0] : start[0] : -1, w + start[1] : start[1] : -1],
]
result = 0
for quarter in quarters:

    @cache
    def possible_pos2(start, n_steps):
        return possible_pos(quarter, start, n_steps)

    for column in trange(n_steps // w + 1):
        n_rows = (n_steps - w * column) // h

        result += (column + 1) * possible_pos2(column * w, n_steps)

result -= 4 * ((n_steps + 1) // 2)

print(result)
