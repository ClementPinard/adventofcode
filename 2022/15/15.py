import numpy as np
from tqdm import trange

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

sensors = []
beacons = []
for line in input_data:
    line = line.split()
    x, y = line[2], line[3]
    x = int(x[2:-1])
    y = int(y[2:-1])
    sensors.append((x, y))

    x, y = line[8], line[9]
    x = int(x[2:-1])
    y = int(y[2:])
    beacons.append((x, y))

sensors = np.array(sensors)
beacons = np.array(beacons)
distance = np.abs(sensors - beacons).sum(axis=1)


def get_impossible(y):
    impossible_x_bins = []
    valid_sensors = np.abs(sensors[:, 1] - y) <= distance
    res_dist = distance - np.abs(sensors[:, 1] - y)
    for s, r in zip(sensors[valid_sensors], res_dist[valid_sensors]):
        impossible_x_bins.append([s[0] - r, s[0] + r])

    merged_bins = []
    while impossible_x_bins:
        found = False
        bin1, *impossible_x_bins = impossible_x_bins
        for j, bin2 in enumerate(impossible_x_bins):
            if (bin1[0] - 1 - bin2[1]) * (bin2[0] - 1 - bin1[1]) >= 0:
                impossible_x_bins[j] = [min(bin1[0], bin2[0]), max(bin1[1], bin2[1])]
                found = True
                break
        if not found:
            merged_bins.append(bin1)
    return merged_bins


print(sum(x2 - x1 for x1, x2 in get_impossible(2_000_000)))

max_y = 4_000_000
for i in trange(max_y):
    impossible = get_impossible(i)
    if len(impossible) > 1:
        print(i, impossible)
        x, y = impossible[0][1] + 1, i
        print(x * 4_000_000 + y)
        break
