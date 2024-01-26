with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]
priority = "abcdefghijklmnopqrstuvwxyz"
priority = priority + priority.upper()

sacks = [(line[: len(line) // 2], line[len(line) // 2 :]) for line in input_data]
common_object = [(set(a) & set(b)).pop() for a, b in sacks]
priorities = [priority.index(c) + 1 for c in common_object]
print(sum(priorities))

common_object = [
    (set(a) & set(b) & set(c)).pop()
    for a, b, c in zip(input_data[::3], input_data[1::3], input_data[2::3])
]
priorities = [priority.index(c) + 1 for c in common_object]
print(sum(priorities))
