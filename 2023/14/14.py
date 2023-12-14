from functools import cache

input_data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split("\n")


@cache
def roll_north(line, forward):
    parts = line.split("#")
    new_parts = []
    for p in parts:
        num_rocks = p.count("O")
        if forward:
            new_parts.append("O" * num_rocks + "." * (len(p) - num_rocks))
        else:
            new_parts.append("." * (len(p) - num_rocks) + "O" * num_rocks)
    return "#".join(new_parts)


def roll_array(lines, direction):
    if direction in "NS":
        new_columns = [roll_north("".join(l), direction == "N") for l in zip(*lines)]
        return tuple("".join(c) for c in zip(*new_columns))
    else:
        return tuple(roll_north(l, direction == "W") for l in lines)


@cache
def cycle(lines):
    for d in "NWSE":
        lines = roll_array(lines, d)
    return lines


with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

lines = tuple(input_data)
# Q1
north_rolled = roll_array(input_data, "N")
score = sum(
    "".join(c).count("O") * (len(lines) - i) for i, c in enumerate(north_rolled)
)
print(score)

# Q2
lines_history = []
n_iter = 1000000000
for i in range(n_iter):
    lines = cycle(lines)
    if lines not in lines_history:
        lines_history.append(lines)
    else:
        first_loop = lines_history.index(lines)
        cycle_length = len(lines_history) - first_loop
        break

final_lines_index = first_loop + (n_iter - first_loop - 1) % cycle_length
lines = lines_history[final_lines_index]

score = sum("".join(c).count("O") * (len(lines) - i) for i, c in enumerate(lines))
print(score)
