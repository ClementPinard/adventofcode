import numpy as np

with open("input.txt") as f:
    octopuses = np.array([list(row) for row in f.read().splitlines()], dtype=int)

def step(oct):
    oct = oct+1
    new_flashes = oct == 10
    flashes = np.copy(new_flashes)
    while(True in new_flashes):
        for i, j in zip(*new_flashes.nonzero()):
            oct[max(i-1, 0): i+2, max(j-1, 0): j+2] += 1
        new_flashes = (oct >= 10) & ~flashes
        flashes = flashes | new_flashes
    oct[flashes] = 0
    return oct, flashes.sum() == oct.size

total_flashes = 0
n_step = 0
sync = False
while not sync:
    octopuses, sync = step(octopuses)
    n_step += 1

print(n_step)