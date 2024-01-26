import numpy as np
import matplotlib.pyplot as plt
from itertools import product

input_data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

m = len(input_data) - 1
n = len(input_data[0]) - 1
states = {((0, 0), 0): 0, ((0, 0), 1): 0}
already_visited = set(states.keys())
paths = {k: [] for k in states.keys()}
final_path = []
max_distance = 0

min_dist = 4
max_dist = 10

while states:
    closest = min(states, key=lambda k: (states[k], -k[0][0] - k[0][1]))
    # closest = min(states, key=lambda k: states[k])
    (i, j), dir = closest
    distance = states.pop(closest)
    already_visited.add(closest)

    real_distance = i + j
    if real_distance > max_distance:
        print(i, j)
        max_distance = real_distance

    if (i, j) == (n, m):
        print(distance)
        print(closest)
        final_path = paths[closest]
        break

    for dist, sign in product(range(min_dist, max_dist + 1), (-1, 1)):
        if dir == 0:
            i2 = i
            j2 = j + dist * sign
            if j2 < 0 or j2 >= len(input_data[0]):
                continue
            new_path = [(i, j + sign * (d + 1)) for d in range(dist)]
            heat_loss = sum(int(input_data[i][j + sign * (d + 1)]) for d in range(dist))
            new_dir = 1
        else:
            i2 = i + dist * sign
            j2 = j
            if i2 < 0 or i2 >= len(input_data):
                continue
            new_path = [(i + sign * (d + 1), j) for d in range(dist)]
            heat_loss = sum(int(input_data[i + sign * (d + 1)][j]) for d in range(dist))
            new_dir = 0
        new_state = ((i2, j2), new_dir)
        if new_state in already_visited:
            continue
        if new_state in states and states[new_state] <= distance + heat_loss:
            continue
        states[new_state] = distance + heat_loss
        paths[new_state] = [*paths[closest], *new_path]

result = np.zeros((len(input_data), len(input_data[0])))
for k, (i, j) in enumerate(final_path):
    result[i, j] = k

plt.imshow(result)
plt.show()
