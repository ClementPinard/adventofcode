from itertools import cycle
import numpy as np

input_data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split("\n")

input_data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

input_sequence = input_data[0]

graph = {}
for line in input_data[2:]:
    start, dest = line.split(" = (")
    left, right = dest[:-1].split(", ")
    graph[start] = {"L": left, "R": right}

# Q1
# state = "AAA"
# end = "ZZZ"
# i = 0
# for direction in cycle(input_sequence):
#     i += 1
#     state = graph[state][direction]
#     if state == end:
#         break
# print(i)

# Q2
starts = [s for s in graph if s.endswith("A")]
ends = {s for s in graph if s.endswith("Z")}

cycles = []
remainders = []

for s in starts:
    history = {}
    state = s
    i = 0
    for direction in cycle(input_sequence):
        i += 1
        state = graph[state][direction]
        full_state = (i % len(input_sequence), state)
        if full_state in history:
            break
        else:
            history[full_state] = i
    cycle_length = i - history[full_state]
    cycles.append(cycle_length)
    good_positions = [
        (state[1], k) for state, k in history.items() if state[1].endswith("Z")
    ][:1]
    assert len(good_positions) == 1
    remainders.append(good_positions[0][1] % cycle_length)


# Because fuck this shit
full_cycle = np.lcm.reduce(cycles)
print(full_cycle)

# Find the final number thanks to the chinse remainder theorem
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem
# Note that this does not work since all cycles are not pairwise coprimes,
# but it doesn't matter because it's not needed
# full_sum = 0
# for r, c in zip(remainders, cycles):
#     n_ = full_cycle // c
#     modulo = c % n_
#     i = 0
#     find the number so that n_*i + c*r == 1 % n_
#     while modulo != 1:
#         i += 1
#         modulo = (modulo + c) % n_
#     full_sum += r * c * i

# print(full_sum)
