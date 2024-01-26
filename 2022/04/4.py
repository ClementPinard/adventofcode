import numpy as np
with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

data = np.loadtxt([line.replace("-",",") for line in input_data], delimiter=",", dtype=int).reshape((-1, 2, 2))

#Q1
contained = (data[:, 0, 0] - data[:, 1, 0]) * (data[:, 0, 1] - data[:, 1, 1]) <= 0
print(contained.sum())

#Q2
overlap = (data[:, 0, 1] - data[:, 1, 0]) * (data[:, 0, 0] - data[:, 1, 1]) <= 0
print(overlap.sum())