import numpy as np
from itertools import cycle

with open("input.txt") as f:
    input_data = f.read()[:-1]

canvas = np.zeros((7, 10))
highest_point = 0
new_piece = True

pieces = [
    [[0, 0], [1, 0], [2, 0], [3, 0]],
    [[1, 2], [0, 1], [1, 1], [2, 1], [1, 0]],
    [[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]],
    [[0, 3], [0, 2], [0, 1], [0, 0]],
    [[0, 1], [1, 1], [0, 0], [1, 0]],
]

pieces = cycle(pieces)
wind = cycle([[1, 0] if c == ">" else [-1, 0] for c in input_data])


def check_pos(piece, position):
    blocks = piece + position
    if blocks[:, 1].min() < 0 or blocks[:, 0].min() < 0 or blocks[:, 0].max() > 6:
        return False
    return canvas[blocks[:, 0], blocks[:, 1]].sum() == 0


def move_piece(piece, position, wind):
    if check_pos(piece, position + wind):
        position += wind
    if check_pos(piece, position + [0, -1]):
        return False, position + [0, -1]
    else:
        return True, position


highest_point_history = []
i = 0
while True:
    if new_piece:
        i += 1
        if i == 2022:
            print(highest_point)
        if i == 1e4:
            break
        piece = np.array(next(pieces), dtype=int)
        position = np.array([2, highest_point + 3], dtype=int)
        if position[1] + 3 >= canvas.shape[1]:
            canvas = np.concatenate((canvas, np.zeros((7, 10))), axis=1)
    new_piece, position = move_piece(piece, position, next(wind))
    if new_piece:
        to_draw = position + piece
        canvas[to_draw[:, 0], to_draw[:, 1]] = 1
        highest_point = max(highest_point, 1 + to_draw[:, 1].max())
        highest_point_history.append(highest_point)

highest_point_history = np.array(highest_point_history)

# Find the repeating pattern
# If we find a point in history where the last 2k highest point where changing the same way,
# we have a periodic derivative and thus can easily deduce highest point for very big numbers
period = 1
data = highest_point_history[-2000:] - highest_point_history[-2000]
while not np.array_equal(
    highest_point_history[-2000 - period : -period]
    - highest_point_history[-2000 - period],
    data,
):
    period += 1

period_data = highest_point_history[-period:] - highest_point_history[-period - 1]
print(period, period_data[-1])
number = 1000000000000 - 1e4
n_periods = int(number // period)
rest = int(number % period)
print(highest_point + period_data[-1] * n_periods + period_data[rest])
