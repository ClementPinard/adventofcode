from functools import cmp_to_key

with open("input.txt") as f:
    input_data = f.read().split("\n\n")


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        else:
            return 1 if a > b else -1
    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    elif isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    else:
        for i, j in zip(a, b):
            result = compare(i,j)
            if result == 0:
                continue
            else:
                return result
        return compare(len(a), len(b))

#Q1
comparison = []
packet_list = []
for pair in input_data:
    a, b = pair.split()
    a, b = eval(a), eval(b)
    packet_list.extend([a,b])
    comparison.append(compare(a, b))
print(sum([i + 1 for i, comp in enumerate(comparison) if comp == -1]))

#Q2
packet_list.extend([[[2]], [[6]]])
sorted_pl = sorted(packet_list, key = cmp_to_key(compare))
print("\n".join(map(str,sorted_pl)))
print((sorted_pl.index([[2]]) + 1)*(sorted_pl.index([[6]]) + 1))
