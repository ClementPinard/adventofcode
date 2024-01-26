import numpy as np

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

score = np.array([0, 0], dtype=int)
for line in input_data:
    a = np.fromstring(line, sep=" ", dtype=int)
    diffs = [a]
    current = a
    while np.abs(current).max() > 0:
        current = current[1:] - current[:-1]
        diffs.append(current)
    extrapolation = np.array([0, 0])
    for d in diffs[::-1]:
        extrapolation = d[[0, -1]] + extrapolation * [-1, 1]
    score += extrapolation
print(score)
