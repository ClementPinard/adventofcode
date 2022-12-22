import numpy as np
import matplotlib.pyplot as plt

debug = False

path = "input2.txt" if debug else "input.txt"
with open(path) as f:
    input_data, commands = f.read()[:-1].split("\n\n")

input_data = input_data.split("\n")
max_char_length = max(map(len, input_data))
input_data = [i + " " * (max_char_length - len(i)) for i in input_data]
commands = commands.replace("L", " L ").replace("R", " R ").split()

xboundaries = []
yboundaries = []


def find_boundaries(data):
    boundaries = []
    for line in data:
        line = "".join(line)
        xmin, xmax = len(line), 0
        if "." in line:
            xmin, xmax = min(xmin, line.find(".")), max(xmax, line.rfind(".") + 1)
        if "#" in line:
            xmin, xmax = min(xmin, line.find("#")), max(xmax, line.rfind("#") + 1)
        boundaries.append([xmin, xmax])
    return boundaries


xboundaries = np.array(find_boundaries(input_data))
yboundaries = np.array(find_boundaries(zip(*input_data)))

canvas = np.zeros((len(input_data), max_char_length), dtype=int)
for i, (xmin, xmax) in enumerate(xboundaries):
    canvas[i, xmin:xmax] = list(map(lambda x: 47 - ord(x), input_data[i][xmin:xmax]))

visited = np.copy(canvas)


class pos:
    position = np.array([0, xboundaries[0, 0]])
    orientation = 0
    directions = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])

    def turn(self, right):
        if right:
            self.orientation += 1
        else:
            self.orientation -= 1
        self.orientation = self.orientation % 4

    def move(self, n_steps):
        d = self.directions[self.orientation]
        sight = np.linspace(self.position, self.position + d * n_steps, n_steps + 1).T
        sight = sight.round().astype(int)
        if d[0]:
            ymin, ymax = yboundaries[self.position[1]]
            sight[0] = (sight[0] - ymin) % (ymax - ymin) + ymin
        else:
            xmin, xmax = xboundaries[self.position[0]]
            sight[1] = (sight[1] - xmin) % (xmax - xmin) + xmin
        path = canvas[sight[0], sight[1]]
        wall = (path == 12).argmax()
        if wall > 0:
            n_steps = min(n_steps, wall - 1)
        self.position = sight[:, n_steps]
        visited[sight[:, : n_steps + 1][0], sight[:, : n_steps + 1][1]] = 20


current_pos = pos()
for c in commands:
    if c.isdigit():
        current_pos.move(int(c))
    else:
        assert c in ["L", "R"]
        current_pos.turn(c == "R")
i, j = current_pos.position + 1
print(current_pos.position, current_pos.orientation)
print(1000 * i + 4 * j + current_pos.orientation)

plt.figure()
plt.imshow(visited)

visisted2 = np.copy(canvas)
if debug:
    face_size = 4
    faces_coords = {1: [0, 2], 2: [1, 0], 3: [1, 1], 4: [1, 2], 5: [2, 2], 6: [2, 3]}

    changes = {
        1: [[3, 3], [6, 2], [2, 2], [4, 0]],
        2: [[6, 1], [3, 0], [1, 2], [5, 2]],
        3: [[2, 0], [4, 0], [1, 1], [5, 3]],
        4: [[3, 0], [6, 1], [1, 0], [5, 0]],
        5: [[3, 1], [6, 0], [4, 0], [2, 2]],
        6: [[5, 0], [1, 2], [4, 3], [2, 3]],
    }
else:
    face_size = 50
    faces_coords = {
        1: [0, 1],
        2: [0, 2],
        3: [1, 1],
        4: [2, 0],
        5: [2, 1],
        6: [3, 0],
    }

    changes = {
        1: [[4, 2], [2, 0], [6, 1], [3, 0]],
        2: [[1, 0], [5, 2], [6, 0], [3, 1]],
        3: [[4, 3], [2, 3], [1, 0], [5, 0]],
        4: [[1, 2], [5, 0], [3, 1], [6, 0]],
        5: [[4, 0], [2, 2], [3, 0], [6, 1]],
        6: [[1, 3], [5, 3], [4, 0], [2, 0]],
    }

faces = np.zeros_like(canvas)
faces_coords = {
    k: np.array([face_size * i, face_size * j]) for k, (i, j) in faces_coords.items()
}
for face_id, (i, j) in faces_coords.items():
    faces[i : i + face_size, j : j + face_size] = face_id
plt.figure()
plt.imshow(faces)


def rotation(pos, orientation):
    if orientation == 0:
        return pos
    elif orientation == 1:
        return [pos[1], face_size - 1 - pos[0]]
    elif orientation == 2:
        return [face_size - 1 - pos[0], face_size - 1 - pos[1]]
    else:
        return [face_size - 1 - pos[1], pos[0]]


class pos_cube(pos):
    face = 1
    position = np.array([0, 0])

    def move_by_one(self):
        new_position = self.position + self.directions[self.orientation]
        new_face = self.face
        or_change = 0
        if new_position[0] < 0:
            new_face, or_change = changes[self.face][2]
            new_position = rotation([face_size - 1, new_position[1]], or_change)
        elif new_position[0] >= face_size:
            new_face, or_change = changes[self.face][3]
            new_position = rotation([0, new_position[1]], or_change)
        elif new_position[1] < 0:
            new_face, or_change = changes[self.face][0]
            new_position = rotation([new_position[0], face_size - 1], or_change)
        elif new_position[1] >= face_size:
            new_face, or_change = changes[self.face][1]
            new_position = rotation([new_position[0], 0], or_change)

        actual_position = new_position + faces_coords[new_face]
        if canvas[actual_position[0], actual_position[1]] == 1:
            self.face = new_face
            self.orientation = (self.orientation + or_change) % 4
            self.position = np.array(new_position)
            visisted2[actual_position[0], actual_position[1]] = 20

    def move(self, n_steps):
        for i in range(n_steps):
            self.move_by_one()


current_pos = pos_cube()
i, j = current_pos.position + faces_coords[current_pos.face]
visisted2[i, j] = 20
for c in commands:
    if c.isdigit():
        current_pos.move(int(c))
    else:
        assert c in ["L", "R"]
        current_pos.turn(c == "R")
i, j = current_pos.position + faces_coords[current_pos.face] + 1
print(i, j, current_pos.orientation)
print(1000 * i + 4 * j + current_pos.orientation)

plt.figure()
plt.imshow(visisted2)
plt.show()
