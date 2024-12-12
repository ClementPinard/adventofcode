from itertools import product

with open("input.txt") as f:
    input_data = f.read().strip().split()

all_filled = set()
h, w = len(input_data), len(input_data[0])


def fill(
    start_pos: tuple[int, int],
    value: int,
    current_filled: set[tuple[int, int]],
    current_frontiers: set[tuple[tuple[int, int], tuple[int, int]]],
) -> tuple[int, int]:
    area, perimeter, sides = 1, 0, 0
    for i, j in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        new_pos = (start_pos[0] + i, start_pos[1] + j)
        if new_pos in current_filled:
            continue
        if (
            new_pos[0] < 0
            or new_pos[1] < 0
            or new_pos[0] >= h
            or new_pos[1] >= w
            or input_data[new_pos[0]][new_pos[1]] != value
        ):
            perimeter += 1
            new_frontier = (start_pos, new_pos)
            adjacents = (
                (
                    (start_pos[0] - j, start_pos[1] + i),
                    (start_pos[0] - j + i, start_pos[1] + i + j),
                ),
                (
                    (start_pos[0] + j, start_pos[1] - i),
                    (start_pos[0] + j + i, start_pos[1] - i + j),
                ),
            )
            sides += 1
            for a in adjacents:
                if a in current_frontiers:
                    sides -= 1
            current_frontiers.add(new_frontier)
        else:
            current_filled.add(new_pos)
            new_area, new_perimeter, new_sides = fill(
                new_pos, value, current_filled, current_frontiers
            )
            area += new_area
            perimeter += new_perimeter
            sides += new_sides
    return area, perimeter, sides


result1, result2 = 0, 0
for i, j in product(range(len(input_data)), range(len(input_data[0]))):
    if (i, j) in all_filled:
        continue
    current_filled = {(i, j)}
    frontiers = set()
    area, perimeter, sides = fill((i, j), input_data[i][j], current_filled, frontiers)
    result1 += area * perimeter
    result2 += area * sides
    all_filled = all_filled.union(current_filled)

print(result1, result2)
