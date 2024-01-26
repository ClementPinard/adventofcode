with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

h, w = len(input_data) - 2, len(input_data[0]) - 2
start = complex(0, 1)
finish = complex(len(input_data) - 1, len(input_data[0]) - 2)

blizzards = []
dir_dict = {
    "<": complex(0, -1),
    ">": complex(0, 1),
    "^": complex(-1, 0),
    "v": complex(1, 0),
}
dir_dict2 = {v: k for k, v in dir_dict.items()}
directions = set(list(dir_dict.values()) + [complex(0, 0)])
wind_directions = []
walls = []
for i, line in enumerate(input_data):
    for j, char in enumerate(line):
        if char in "<>^v":
            blizzards.append(complex(i, j))
            wind_directions.append(dir_dict[char])
        elif char == "#":
            walls.append(complex(i, j))

walls.extend([complex(-1, j) for j in range(w + 2)])
walls.extend([complex(h + 2, j) for j in range(w + 2)])
walls.extend([complex(j, -1) for j in range(h + 2)])
walls.extend([complex(j, w + 2) for j in range(h + 2)])
blizzards = tuple(blizzards)
wind_directions = tuple(wind_directions)
walls = set(walls)


def update_wind(blizzards, wind_directions):
    new_blizzards = [b + d for b, d in zip(blizzards, wind_directions)]
    return tuple(
        complex(1 + (c.real - 1) % h, 1 + (c.imag - 1) % w) for c in new_blizzards
    )


blizzards_list = [blizzards]
while True:
    new_blizzard = update_wind(blizzards_list[-1], wind_directions)
    if new_blizzard == blizzards_list[0]:
        break
    else:
        blizzards_list.append(new_blizzard)

def plot(positions, blizz, wind_directions):
    plot_string = (
        [[*input_data[0]]]
        + [[*("#" + "." * w + "#")] for _ in range(h)]
        + [[*input_data[-1]]]
    )

    for b, d in zip(blizz, wind_directions):
        i, j = int(b.real), int(b.imag)
        char = plot_string[i][j]
        if char == ".":
            plot_string[i][j] = dir_dict2[d]
        elif char in "<>^v":
            plot_string[i][j] = "2"
        else:
            plot_string[i][j] = chr(ord(char) + 1)
    for p in positions:
        i, j = int(p.real), int(p.imag)
        char = plot_string[i][j]
        plot_string[i][j] = "E" if char == "." else "A"
    print("\n".join("".join(line) for line in plot_string))


# for b in blizzards_list:
#     plot([], b, wind_directions)


def can_move(position, blizzards, walls):
    candidates = {position + d for d in directions} - blizzards - walls
    return candidates

blizzards_list = [set(b) for b in blizzards_list]
n = len(blizzards_list)

def go_through(start, finish, blizzard_state):
    i = blizzard_state
    candidates = {start}
    while finish not in candidates:
        i += 1
        candidates = set().union(
            *[can_move(c, blizzards_list[i % n], walls) for c in candidates]
        )
    return i

steps = 0
steps = go_through(start, finish, steps)
print(steps)
steps = go_through(finish, start, steps)
print(steps)
steps = go_through(start, finish, steps)
print(steps)