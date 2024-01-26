from collections import defaultdict
import numpy as np

input_data = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

supperted_by = defaultdict(set)
supports = defaultdict(set)


def intersect(b1, b2):
    result = bool(
        set(tuple(c) for c in b1[:, :2].tolist())
        & set(tuple(c) for c in b2[:, :2].tolist())
    )
    return result


bricks = []
for line in input_data:
    start, end = line.split("~")
    xs, ys, zs = map(int, start.split(","))
    xe, ye, ze = map(int, end.split(","))
    if xs != xe:
        brick = np.array([[x, ys, zs] for x in range(min(xs, xe), max(xs, xe) + 1)])
    elif ys != ye:
        brick = np.array([[xs, y, zs] for y in range(min(ys, ye), max(ys, ye) + 1)])
    else:
        brick = np.array([[xs, ys, z] for z in range(min(zs, ze), max(zs, ze) + 1)])
    bricks.append(brick)

bricks = sorted(bricks, key=lambda x: x[:, 2].min())
grounded_bricks = []
for j, b in enumerate(bricks):
    z = 0
    candidates = []
    for i, b2 in enumerate(grounded_bricks):
        if intersect(b, b2):
            z = max(z, b2[:, 2].max())
            candidates.append(i)
    grounded_brick = np.copy(b)
    grounded_brick[:, 2] -= grounded_brick[:, 2].min() - z - 1
    grounded_bricks.append(grounded_brick)
    for i in candidates:
        if grounded_bricks[i][:, 2].max() == z:
            supperted_by[j].add(i)
            supports[i].add(j)

# Q1
result = 0
for i in range(len(bricks)):
    possible = True
    for k, v in supperted_by.items():
        if i in v and len(v) == 1:
            possible = False
    if possible:
        result += 1
print(result)

# Q2
result = 0
for i in range(len(bricks)):
    fallen_bricks = {i}
    to_fall = supports[i]
    while to_fall:
        next_to_fall = to_fall.pop()
        if supperted_by[next_to_fall] - set.union(fallen_bricks, {next_to_fall}):
            continue
        to_fall.update(supports[next_to_fall])
        fallen_bricks.add(next_to_fall)
    result += len(fallen_bricks) - 1

print(result)
