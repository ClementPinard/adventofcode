from itertools import product
from collections import defaultdict

input_data = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

start_pos = (0, input_data[0].find("."))
end = (len(input_data) - 1, input_data[-1].find("."))


def possible_next_tiles(i0, j0):
    possible = set()
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_tile = (i0 + i, j0 + j)
        if (
            next_tile[0] < 0
            or next_tile[0] >= len(input_data)
            or next_tile[1] < 0
            or next_tile[1] >= len(input_data[0])
        ):
            continue
        next_tile_value = input_data[next_tile[0]][next_tile[1]]
        if next_tile_value == "#":
            continue
        possible.add(next_tile)
    return possible


def travel_tunnel(start, direction, slippery=False):
    current = start[0] + direction[0], start[1] + direction[1]
    previous = start
    length = 1
    while True:
        possible_next = possible_next_tiles(*current)
        if len(possible_next) == 1:
            if current in {start_pos, end}:
                return (current, length + 1)
            return None, None
        elif len(possible_next) == 2:
            current, previous = (
                min(possible_next, key=lambda x: x == previous),
                current,
            )
            length += 1
            if slippery:
                if (
                    current[0] - previous[0] == -1
                    and input_data[current[0]][current[1]] == "v"
                ) or (
                    current[1] - previous[1] == -1
                    and input_data[current[0]][current[1]] == ">"
                ):
                    return None, None
        else:
            return (current, length)


graph = defaultdict(dict)

for i, j in product(range(len(input_data)), range(len(input_data[0]))):
    if input_data[i][j] == "#":
        continue
    possible_next = possible_next_tiles(i, j)
    if len(possible_next) <= 2:
        continue
    else:
        for p in possible_next:
            # Q1
            # slippery = True
            # Q2
            slippery = False
            dest, length = travel_tunnel(
                (i, j), (p[0] - i, p[1] - j), slippery=slippery
            )
            if dest is not None:
                graph[(i, j)][dest] = length
                if dest in {start_pos, end}:
                    graph[dest][(i, j)] = length


first_state = (frozenset(), start_pos)
states = {first_state}
lengths = {first_state: 0}
max_length = 0
while states:
    state = max(states, key=lambda x: lengths[x])
    states.remove(state)
    visited, current = state
    for dest, distance in graph[current].items():
        if dest in visited:
            continue
        new_distance = lengths[state] + distance
        next_state = visited | {dest}, dest
        if next_state in lengths and lengths[next_state] >= new_distance:
            continue
        lengths[next_state] = new_distance
        states.add(next_state)

    if current == end:
        if lengths[state] > max_length:
            max_length = lengths[state]
            print(max_length - 2)
valid_length = {x: v for x, v in lengths.items() if x[1] == end}
print(max(valid_length.values()) - 2)
