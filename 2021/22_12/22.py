import numpy as np

with open('input.txt') as f:
    input_lines = f.read().splitlines()

def parse(s):
    point = s.find('.')
    return int(s[2:point]),int(s[point+2:]) + 1

cubes = []
commands = []
for line in input_lines:
    command, rest = line.split(" ")
    command = 1 if command == "on" else 0
    cubes.append(list(map(parse, rest.split(','))))
    commands.append(command)

cubes = np.array(cubes)
X = np.unique(np.sort(cubes[:, 0].flatten()))
Y = np.unique(np.sort(cubes[:, 1].flatten()))
Z = np.unique(np.sort(cubes[:, 2].flatten()))
cub_sizes = np.ones((len(X)-1, len(Y)-1, len(Z)-1), dtype=int)
cub_sizes *= Z[1:] - Z[:-1]
cub_sizes *= (Y[1:] - Y[:-1])[:, None]
cub_sizes *= (X[1:] - X[:-1])[:, None, None]
lights = np.zeros((len(X)-1, len(Y)-1, len(Z)-1), dtype=int)
for cube, command in zip(cubes, commands):
    x1, x2 = np.searchsorted(X, cube[0])
    y1, y2 = np.searchsorted(Y, cube[1])
    z1, z2 = np.searchsorted(Z, cube[2])
    lights[x1:x2, y1:y2, z1:z2] = command
print((lights * cub_sizes).sum())