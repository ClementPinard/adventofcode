import numpy as np

input_data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".split("\n\n")

with open("input.txt") as f:
    input_data = f.read().split("\n\n")


def find_symmetry(input_array, q):
    h = input_array.shape[0]
    for i in range(1, h):
        top_side = input_array[max(0, 2 * i - h) : i]
        bottom_side = input_array[i : min(h, 2 * i)]
        if (top_side != bottom_side[::-1]).sum() == (0 if q == 1 else 1):
            return i
    return 0


mapping_dict = {"#": 1, ".": 0}
scores = [0, 0]

for input_pattern in input_data:
    lines = input_pattern.split("\n")
    if not lines[-1]:
        lines = lines[:-1]
    input_pattern = np.array([[mapping_dict[c] for c in line] for line in lines])

    for q in [1, 2]:
        h_sym = find_symmetry(input_pattern, q)
        if h_sym == 0:
            v_sym = find_symmetry(input_pattern.T, q)
        else:
            v_sym = 0
        scores[q - 1] += v_sym + 100 * h_sym
print(scores)
