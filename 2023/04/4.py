import numpy as np


def to_numbers(line):
    split = line.split(" ")
    return set(map(int, [s for s in split if s]))


def get_wins(line):
    winning, numbers = line.split(" | ")
    winning = winning.split(": ")[1]
    winning = to_numbers(winning)
    numbers = to_numbers(numbers)
    return len(winning & numbers)


with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

# Q1
score = 0
for line in input_data:
    n_win = get_wins(line)
    if n_win > 0:
        score += np.power(2, n_win - 1)
print(score)

# Q2
copies = len(input_data)
transfer_matrix = np.zeros((copies, copies))
for i, line in enumerate(input_data):
    n_win = get_wins(line)
    transfer_matrix[i + 1 : i + 1 + n_win, i] = 1

state = np.ones((copies, 1))
state_sum = state.sum()
score = 0
while state_sum > 0:
    state_sum = state.sum()
    score += int(state_sum)
    state = transfer_matrix @ state

print(score)
