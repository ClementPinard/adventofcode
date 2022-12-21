from yaml import safe_load
from numpy.polynomial import Polynomial
from copy import deepcopy

with open("input.txt") as f:
    input_data = safe_load(f)

for n in input_data:
    try:
        input_data[n] = int(input_data[n])
    except ValueError:
        pass


def yell(data, node):
    value = data[node]
    if isinstance(value, (int, Polynomial)):
        return value
    m1, op, m2 = value.split()
    v1 = yell(data, m1)
    v2 = yell(data, m2)

    if op == "+":
        result = v1 + v2
    elif op == "/":
        result = v1 // v2
    elif op == "-":
        result = v1 - v2
    elif op == "*":
        result = v1 * v2
    data[value] = result
    return result


Q1_data = deepcopy(input_data)

print(yell(Q1_data, "root"))

# Q2
Q2_data = deepcopy(input_data)
Q2_data["root"] = input_data["root"].replace("+", "-")
Q2_data["humn"] = Polynomial([0, 1])

print(Q2_data)

result = yell(Q2_data, "root")
print(result)
solution = result.roots()[0]
print(round(solution))
