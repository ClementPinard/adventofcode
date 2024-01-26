import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes

input_data = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".split("\n")


with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

input_data = np.array([list(i) for i in input_data])


def plot(right, left, path):
    a = np.zeros((input_data.shape[0] + 2, input_data.shape[1] + 2), dtype=float)
    for i, j in left:
        a[i + 1, j + 1] = 1
    for i, j in right:
        a[i + 1, j + 1] = 2
    for i, j in path:
        a[i + 1, j + 1] = -1
    plt.imshow(a)
    plt.colorbar()
    plt.show()


connexions = {
    "L": [[-1, 0], [0, 1]],
    "J": [[0, -1], [-1, 0]],
    "7": [[0, -1], [1, 0]],
    "|": [[1, 0], [-1, 0]],
    "-": [[0, -1], [0, 1]],
    "F": [[1, 0], [0, 1]],
    ".": [],
}

right = {
    "L": [[0, -1], [1, -1], [1, 0]],
    "J": [[1, 0], [1, 1], [0, 1]],
    "7": [],
    "|": [[0, 1]],
    "-": [[1, 0]],
    "F": [],
}

left = {
    "L": [],
    "J": [],
    "7": [[-1, 0], [-1, 1], [0, 1]],
    "|": [[0, -1]],
    "-": [[-1, 0]],
    "F": [[0, -1], [-1, -1], [-1, 0]],
}

S_pos = np.array(np.where(input_data == "S"))[:, 0]
i = S_pos[0]
j = S_pos[1]
possible_pipes = set([*"LJ7|-F"])
if [-1, 0] in connexions[str(input_data[i + 1, j])]:
    possible_pipes -= set([*"LJ|"])
if [1, 0] in connexions[str(input_data[i - 1, j])]:
    possible_pipes -= set([*"7F|"])
if [0, 1] in connexions[str(input_data[i, j - 1])]:
    possible_pipes -= set([*"LF-"])
if [0, -1] in connexions[str(input_data[i, j + 1])]:
    possible_pipes -= set([*"J7-"])

s_tile = list(possible_pipes)[0]
print(s_tile)
previous_pos = S_pos
current_pos = S_pos + connexions[s_tile][0]
print(current_pos)
path = {(i, j), tuple(current_pos)}
left_interior = set()
right_interior = set()
length = 0
while not np.array_equal(current_pos, S_pos):
    pipe = input_data[tuple(current_pos)]
    displacement = connexions[pipe]
    next_pos = current_pos + displacement
    if np.array_equal(next_pos[0], previous_pos):
        previous_pos = current_pos
        current_pos = next_pos[1]
        invert_left = False
    else:
        previous_pos = current_pos
        current_pos = next_pos[0]
        invert_left = True

    for r in right[pipe]:
        if invert_left:
            left_interior.add(tuple(previous_pos + r))
        else:
            right_interior.add(tuple(previous_pos + r))
    for l in left[pipe]:
        if invert_left:
            right_interior.add(tuple(previous_pos + l))
        else:
            left_interior.add(tuple(previous_pos + l))
    path.add(tuple(current_pos))
if max(left_interior) > max(right_interior):
    inner_interior = right_interior
else:
    inner_interior = left_interior
inner_interior = inner_interior - path
result = np.zeros_like(input_data, dtype=int)
for i in inner_interior:
    result[i] = 1

plot(right_interior, left_interior, path)
result = binary_fill_holes(result)
plt.imshow(result)
plt.show()

print(result.sum())
