import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

input_data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

mapping_dict = {k: v for k, v in zip("./\\-|", np.eye(5)[:, 1:])}
print(mapping_dict)
input_data = list(
    np.array(
        [list(map(lambda x: mapping_dict[x], line)) for line in input_data]
    ).transpose(2, 0, 1)
)


def turn_left(array, position, energized):
    new_array = [np.fliplr(np.transpose(array[i])) for i in [1, 0, 3, 2]]
    new_energized = [np.fliplr(np.transpose(energized[i])) for i in [1, 2, 3, 0]]
    new_position = (position[1], array[0].shape[0] - position[0] - 1)
    updated_energized = beam(new_array, new_position, new_energized)
    return [np.transpose(updated_energized[i])[::-1] for i in [3, 0, 1, 2]]


def turn_right(array, position, energized):
    new_array = [np.transpose(array[i]) for i in [0, 1, 3, 2]]
    new_energized = [np.transpose(energized[i]) for i in [3, 2, 1, 0]]
    new_position = (position[1], position[0])
    updated_energized = beam(new_array, new_position, new_energized)
    return [np.transpose(updated_energized[i]) for i in [3, 2, 1, 0]]


def beam(array, position, energized):
    if position[1] >= array[0].shape[1] - 1:
        return energized
    first_beam = [a[position[0], position[1] + 1 :] for a in array]
    obstacle_pos = array[0].shape[1]
    for f in first_beam:
        if (f > 0).sum() == 0:
            continue
        obstacle_pos = min(obstacle_pos, (f > 0).nonzero()[0][0])
    obstacle_pos += position[1] + 1
    if True in energized[0][position[0], position[1] + 1 : obstacle_pos + 1]:
        energized[0][position[0], position[1] + 1 : obstacle_pos + 1] = True
        return energized
    energized[0][position[0], position[1] + 1 : obstacle_pos + 1] = True
    if obstacle_pos >= array[0].shape[1]:
        return energized
    obstacle = [a[position[0], obstacle_pos] for a in array]
    if obstacle[0] == 1:
        return turn_left(array, (position[0], obstacle_pos), energized)
    elif obstacle[1] == 1:
        return turn_right(array, (position[0], obstacle_pos), energized)
    elif obstacle[2] == 1:
        return beam(array, (position[0], obstacle_pos), energized)
    else:
        energized_left = turn_left(array, (position[0], obstacle_pos), energized)
        energized_right = turn_right(array, (position[0], obstacle_pos), energized)
        return [e1 | e2 for e1, e2 in zip(energized_left, energized_right)]


def get_n_energized(input_array, start):
    energized = [np.zeros_like(i, dtype=bool) for i in input_array[:4]]
    result = beam(input_data, (start, -1), energized)
    return (sum(result) > 0).sum()


energized = [np.zeros_like(i, dtype=bool) for i in input_data[:4]]
result = beam(input_data, (0, -1), energized)
plt.imshow(sum(result))
plt.show()
print(get_n_energized(input_data, 0))

most_energized = 0
flipped = [input_data[i][:, ::-1] for i in [1, 0, 2, 3]]
for i in trange(input_data[0].shape[0]):
    most_energized = max(most_energized, get_n_energized(input_data, i))
    most_energized = max(most_energized, get_n_energized(flipped, i))

input_data_t = [np.transpose(i) for i in input_data]
flipped_t = [input_data_t[i][:, ::-1] for i in [1, 0, 2, 3]]

for i in trange(input_data[0].shape[1]):
    most_energized = max(most_energized, get_n_energized(input_data_t, i))
    most_energized = max(most_energized, get_n_energized(flipped_t, i))

print(most_energized)
