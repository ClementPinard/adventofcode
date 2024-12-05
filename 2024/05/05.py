from collections import defaultdict

with open("input.txt") as f:
    orders, updates = f.read()[:-1].split("\n\n")

order_dict = defaultdict(set)
for line in orders.split():
    a, b = line.split("|")
    order_dict[a].add(b)


def reorder(numbers_set: set):
    if len(numbers_set) <= 1:
        return list(numbers_set)
    middle = numbers_set.pop()
    right = order_dict[middle].intersection(numbers_set)
    left = numbers_set - order_dict[middle]
    return [*reorder(right), middle, *reorder(left)]


result_q1 = 0
result_q2 = 0
for line in updates.split():
    numbers = line.split(",")
    good = True
    for i, number in enumerate(numbers):
        before = set(numbers[:i])
        if before.intersection(order_dict[number]):
            good = False
            break
    if good:
        result_q1 += int(numbers[len(numbers) // 2])
    else:
        result_q2 += int(reorder(set(numbers))[len(numbers) // 2])

print(result_q1)
print(result_q2)
