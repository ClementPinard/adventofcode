import numpy as np

with open("input.txt") as f:
    input_data = f.read()[:-1].split("\n\n")


def map_to_func(text):
    data = np.stack(
        [np.fromstring(line, dtype=int, sep=" ") for line in text.split("\n")]
    )

    def func(n):
        for line in data:
            if n >= line[1] and n < line[1] + line[2]:
                return line[0] + n - line[1]
        else:
            return n

    return func


seeds = list(map(int, input_data[0].split(": ")[1].split(" ")))


funcs = []
for map_string in input_data[1:]:
    funcs.append(map_to_func(map_string.split(":\n")[1]))

# Q1
soils = []
for s in seeds:
    for f in funcs:
        s = f(s)
    soils.append(s)

print(min(soils))


# Q2
def merge_ranges(ranges):
    r = sorted(ranges, key=lambda x: x[0])
    merged = []
    while True:
        first_range = r.pop(0)
        if not r:
            merged.append(first_range)
            break
        if first_range[1] >= r[0][0]:
            r[0][0] = first_range[0]
            r[0][1] = max(r[0][1], first_range[1])
        else:
            merged.append(first_range)
    return merged


def map_to_range_func(text):
    data = np.stack(
        [np.fromstring(line, dtype=int, sep=" ") for line in text.split("\n")]
    )
    data = sorted(data, key=lambda x: x[1])

    def func(input_ranges):
        ranges = []
        for n1, n2 in input_ranges:
            for line in data:
                min_source = line[1]
                max_source = line[1] + line[2]
                if n1 < min_source:
                    ranges.append([n1, min(min_source - 1, n2)])
                    n1 = min_source
                if n1 < max_source:
                    ranges.append(
                        [
                            max(0, n1 - min_source) + line[0],
                            min(n2 - min_source, line[2] - 1) + line[0],
                        ]
                    )
                    if n2 < max_source:
                        break
                    else:
                        n1 = max_source
            last_max_source = data[-1][1] + data[-1][2]
            if n2 >= last_max_source:
                ranges.append([max(last_max_source, n1), n2])
        return merge_ranges(ranges)

    return func


range_funcs = []
for map_string in input_data[1:]:
    range_funcs.append(map_to_range_func(map_string.split(":\n")[1]))

soil_ranges = []
for s1, s2 in zip(seeds[::2], seeds[1::2]):
    s_ranges = [[s1, s1 + s2]]
    for f in range_funcs:
        s_ranges = f(s_ranges)
    soil_ranges.extend(merge_ranges(s_ranges))


print(min(soil_ranges, key=lambda x: x[0]))
