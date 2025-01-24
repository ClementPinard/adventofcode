import numpy as np
import matplotlib.pyplot as plt


def hashable(position, direction):
    return tuple(position.tolist() + direction.tolist())


with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

mapping = {"#": 0, ".": 1, "S": 2, "E": 3}
input_data = list(map(lambda x: [mapping[c] for c in x], input_data))
input_array = np.array(input_data)

S_pos = np.concatenate((input_array == 2).nonzero())
input_array[*S_pos] = 1
E_pos = np.concatenate((input_array == 3).nonzero())
costs = {}
start_direction = np.array([0, 1])
path_histories = {hashable(S_pos, start_direction): {tuple(S_pos.tolist())}}
turn_right = np.array([[0, -1], [1, 0]])
turn_left = np.array([[0, 1], [-1, 0]])

to_visit = [(S_pos, start_direction, 0)]

path_to_exit = set()

while to_visit:
    to_visit = sorted(to_visit, key=lambda x: x[-1])
    (current_pos, direction, score), *to_visit = to_visit
    history = path_histories[hashable(current_pos, direction)]
    for i, new_direction in enumerate(
        [direction, turn_right @ direction, turn_left @ direction]
    ):
        new_history = history
        new_position = current_pos + new_direction
        if input_array[*new_position] == 0:
            continue
        hash = hashable(new_position, new_direction)
        new_score = score + 1 if i == 0 else score + 1001
        last_score = costs.get(hash, 10000000)
        costs[hash] = min(new_score, last_score)
        new_history = new_history.union({tuple(new_position.tolist())})
        if new_score < last_score:
            path_histories[hash] = new_history
            to_visit.append((new_position, new_direction, new_score))
        elif new_score == last_score:
            path_histories[hash] = path_histories[hash].union(new_history)
        if np.allclose(E_pos, new_position):
            path_to_exit = path_to_exit.union(new_history)


result_array = np.full_like(input_array, 1e6).astype(float)
result_array[input_array == 0] = np.nan
for (x, y, *direction), score in costs.items():
    result_array[x, y] = min(result_array[x, y], score)

plt.imshow(result_array)
plt.colorbar()
plt.show()

print(int(result_array[*E_pos]))

result_array2 = input_array.copy().astype(float)
result_array2[input_array == 0] = np.nan
for (x, y, *direction), history in path_histories.items():
    if x == E_pos[0] and y == E_pos[1]:
        if costs[x, y, *direction] == result_array[*E_pos]:
            for x1, y1 in history:
                result_array2[x1, y1] = 2
plt.imshow(result_array2)
plt.show()

print((result_array2 == 2).sum())
