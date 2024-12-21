import numpy as np

with open("input.txt") as f:
    input_data = f.read().strip().split("\n\n")


result = 0
for bloc in input_data:
    lines = [line.split(": ")[1].split(", ") for line in bloc.split("\n")]
    button_a, button_b, prize = lines
    button_a = [int(button_a[0][1:]), int(button_a[1][1:])]
    button_b = [int(button_b[0][1:]), int(button_b[1][1:])]
    prize = [int(prize[0][2:]), int(prize[1][2:])]

    problem = np.array([button_a, button_b]).T
    target = np.array(prize) + 10000000000000
    solution = np.linalg.solve(problem, target)
    if all(solution.round() == solution.round(3)):
        result += solution[0] * 3 + solution[1]


print(int(result))
