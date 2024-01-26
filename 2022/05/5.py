from collections import defaultdict

with open("input.txt") as f:
    input_data = f.read()[:-1]

crates, commands = input_data.split("\n\n")

crates_dict = defaultdict(list)
numbers, *crates = crates.split("\n")[::-1]
positions = {int(n): numbers.index(n) for n in set(numbers.replace(" ", ""))}
for line in crates:
    for k,v in positions.items():
        crate = line[v]
        if crate != " ":
            crates_dict[k].append(crate)

for c in commands.split("\n"):
    v = int(c[5:c.index(" from")])
    k1 = int(c[c.index("from ") + 5: c.index(" to")])
    k2 = int(c[c.index("to ") + 3:])
    
    #Q1
    #crates_dict[k2].extend(crates_dict[k1][-v:][::-1])
    #Q2
    crates_dict[k2].extend(crates_dict[k1][-v:])
    del crates_dict[k1][-v:]

print(''.join(crates_dict[k][-1] for k in sorted(crates_dict.keys())))