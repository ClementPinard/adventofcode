import numpy as np
import matplotlib.pyplot as plt

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

size = np.array([101, 103])
robots = []
for line in input_data:
    pos, speed = line.split()
    pos = np.fromstring(pos[2:], sep=",", dtype=int)
    speed = np.fromstring(speed[2:], sep=",", dtype=int)
    robots.append([pos, speed])

# Q1
mid_size = size // 2
print(mid_size)
quadrants = np.zeros((2, 2), dtype=int)

for pos, speed in robots:
    last_pos = (pos + speed * 100) % size
    print(last_pos)
    if any(last_pos == mid_size):
        continue
    quad = np.clip(last_pos // mid_size, 0, 1)
    quadrants[*quad] += 1

print(quadrants)
print(quadrants.prod())

# Q2
i = 0
while True:
    i += 1
    print(i)
    canvas = np.zeros(size)
    for pos, speed in robots:
        last_pos = (pos + speed * i) % size
        canvas[*last_pos] = 1
    if canvas.sum() == len(robots):
        plt.imshow(canvas)
        plt.show()
