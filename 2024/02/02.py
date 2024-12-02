import numpy as np

with open("input.txt") as f:
    lines = f.read().split("\n")[:-1]

array: list[np.ndarray] = list(
    map(lambda x: np.fromstring(x, sep=" ", dtype=int), lines)
)


def issafe(input_array: np.ndarray) -> bool:
    diff = input_array[1:] - input_array[:-1]
    if not ((np.abs(diff) >= 1).all() and (np.abs(diff) <= 3).all()):
        return False
    if (diff > 0).all() or (diff < 0).all():
        return True
    return False


# Q1
safe = 0
for row in array:
    safe += int(issafe(row))

print(safe)

# Q2
safe = 0
for row in array:
    if issafe(row):
        safe += 1
        continue
    for i in range(len(row)):
        sub_row = np.concat([row[:i], row[i + 1 :]])
        if issafe(sub_row):
            safe += 1
            break
print(safe)
