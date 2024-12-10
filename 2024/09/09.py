import numpy as np
from tqdm import tqdm

with open("input.txt") as f:
    input_data = list(map(int, f.read().strip()))

# Q1
input_dict = {}
pos = 0
positions = []
for i, (size, free_size) in enumerate(zip(input_data[::2], input_data[1::2] + [0])):
    positions.append(pos)
    input_dict[pos] = (i, size, free_size)
    pos += size + free_size

sorted_dict = np.zeros(sum(input_data), dtype=int) - 1
current_pos = 0
while current_pos <= positions[-1]:
    id, size, free_size = input_dict[current_pos]
    last_position = positions[-1]
    last_id, last_size, _ = input_dict[last_position]
    sorted_dict[current_pos : current_pos + size] = id
    current_pos += size
    if last_size >= free_size:
        sorted_dict[current_pos : current_pos + free_size] = last_id
        if last_size > free_size:
            input_dict[last_position] = (last_id, last_size - free_size, 0)
        else:
            positions.pop()
            input_dict.pop(last_position)
        current_pos += free_size
    else:
        sorted_dict[current_pos : current_pos + last_size] = last_id
        input_dict[current_pos] = (last_id, last_size, free_size - last_size)
        positions.pop()
        input_dict.pop(last_position)

result = sorted_dict * np.arange(len(sorted_dict))
print(result[result >= 0].sum())

# Q2
input_dict = {}
pos = 0
positions = []
free_spaces = {}
for i, (size, free_size) in enumerate(zip(input_data[::2], input_data[1::2] + [0])):
    positions.append(pos)
    input_dict[pos] = (i, size)
    free_spaces[pos + size] = free_size
    pos += size + free_size

sorted_dict = np.zeros(sum(input_data), dtype=int) - 1

breakpoint()
for last_position in tqdm(positions[::-1]):
    id, last_size = input_dict[last_position]
    found = False
    if id == 2:
        breakpoint()
    for pos, free_space in free_spaces.items():
        if pos > last_position:
            break
        if free_space >= last_size:
            new_pos = pos
            found = True
            break

    if not found:
        sorted_dict[last_position : last_position + last_size] = id
        continue
    free_space = free_spaces.pop(new_pos)
    sorted_dict[new_pos : new_pos + last_size] = id
    if last_size < free_space:
        free_spaces[new_pos + last_size] = free_space - last_size
        free_spaces = {k: free_spaces[k] for k in sorted(free_spaces)}

print(sorted_dict[:100])
result = sorted_dict * np.arange(len(sorted_dict))
print(result[result >= 0].sum())
