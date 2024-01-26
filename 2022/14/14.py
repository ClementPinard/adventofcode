import numpy as np

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

coordinates = []
for line in input_data:
    current_coordinates = [
        list(map(int, chunk.split(","))) for chunk in line.split(" -> ")
    ]
    coordinates.append(np.array(current_coordinates))

ymin = min(0, min([c[:, 1].min() for c in coordinates]))
ymax = max([c[:, 1].max() for c in coordinates])
xmin = min([c[:, 0].min() for c in coordinates]) - 1
xmax = max([c[:, 0].max() for c in coordinates]) + 1

Q2 = True
# Q2
if Q2:
    ymax = ymax + 2
    xmin = 500 - ymax
    xmax = 500 + ymax


canvas = np.zeros((xmax - xmin + 1, ymax - ymin + 1))

# Q2
if Q2:
    canvas[:, -1] = 1

for c in coordinates:
    for pos1, pos2 in zip(c, c[1:]):
        distance = np.abs(pos1 - pos2).sum()
        to_draw = np.linspace(pos1, pos2, distance + 1).astype(int)
        canvas[to_draw[:, 0] - xmin, to_draw[:, 1] - ymin] = 1

start_point = np.array([500 - xmin, 0 - ymin])

sand_pos = start_point
candidates = np.array([[0, +1], [-1, +1], [1, +1]])
num_sand = 0
while True:
    if sand_pos[1] == ymax:
        break
    found = False
    for c in candidates:
        c_pos = sand_pos + c
        if canvas[c_pos[0], c_pos[1]] == 0:
            sand_pos = c_pos
            found = True
            break
    if found:
        continue
    if sand_pos[1] == ymax - ymin:
        break
    canvas[sand_pos[0], sand_pos[1]] = 2
    if sand_pos[1] == 0:
        num_sand += 1
        break
    sand_pos = start_point
    num_sand += 1

import matplotlib.pyplot as plt

plt.imshow(canvas.T)
plt.show()
print(num_sand)
