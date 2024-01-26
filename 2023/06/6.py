import numpy as np
from numpy.polynomial import Polynomial

input_data = """Time:      7  15   30
Distance:  9  40  200""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

# Q1
time_values = list(map(int, input_data[0].split(": ")[1].strip().split()))
distance_values = list(map(int, input_data[1].split(": ")[1].strip().split()))

# Q2
time_values = [int(input_data[0].split(": ")[1].replace(" ", ""))]
distance_values = [int(input_data[1].split(": ")[1].replace(" ", ""))]

result = 1
for t, d in zip(time_values, distance_values):
    time_left = Polynomial((t, -1))
    speed = Polynomial((0, 1))
    score = speed * time_left - d
    min_value, max_value = score.roots()
    winning = int(np.ceil(max_value - 1) - np.floor(min_value + 1) + 1)
    result *= winning

print(result)
