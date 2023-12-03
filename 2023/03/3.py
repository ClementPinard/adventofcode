import numpy as np

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

characters = {c: i for i, c in enumerate("0123456789*@=/%+$-#&")}
characters["."] = -1

input_data = np.array([list(characters[c] for c in line) for line in input_data])
h = input_data.shape[0]
m1 = np.full((h, 1), -1)
input_data = np.concatenate([m1, input_data, m1], axis=1)

is_digit = ((input_data >= 0) & (input_data < 10)).astype(int)

diff = is_digit[:, 1:] - is_digit[:, :-1]
number_begins = np.argwhere(diff > 0)
number_ends = np.argwhere(diff < 0)

# Q3
other_numbers = 0
for i_start, i_end in zip(number_begins, number_ends):
    line, k1 = i_start
    k2 = i_end[1]
    k1 += 1
    k2 += 1
    number = int("".join(map(str, input_data[line, k1:k2])))
    near_special = input_data[max(line - 1, 0) : line + 2, k1 - 1 : k2 + 1]
    if (near_special >= 10).sum() > 0:
        other_numbers += number

print(other_numbers)

# Q2
to_multiply = {}
for i_start, i_end in zip(number_begins, number_ends):
    line, k1 = i_start
    k2 = i_end[1]
    k1 += 1
    k2 += 1
    number = int("".join(map(str, input_data[line, k1:k2])))
    near_star = input_data[max(line - 1, 0) : line + 2, k1 - 1 : k2 + 1]
    for i_, j_ in np.argwhere(near_star == 10):
        i = i_ + max(line - 1, 0)
        j = j_ + k1 - 1
        if (i, j) in to_multiply:
            to_multiply[(i, j)].append(number)
        else:
            to_multiply[(i, j)] = [number]
gears = 0
for n in to_multiply.values():
    if len(n) == 2:
        gears += n[0] * n[1]

print(gears)
