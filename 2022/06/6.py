with open("input.txt") as f:
    input_data = f.read()[:-1]

i = 0
while len(set(input_data[i: i+14])) < 14:
    i += 1

print(i+14)