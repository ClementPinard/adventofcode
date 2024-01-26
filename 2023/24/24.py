import numpy as np
from itertools import combinations
from tqdm import tqdm
from sympy import symbols, solve

input_data = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".split("\n")

test_range = [7, 27]

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

test_range = [200000000000000, 400000000000000]


def intersection2D(ray1, ray2):
    p1, v1 = ray1
    p2, v2 = ray2

    d = (p2 - p1)[:2]

    A = np.stack([v1, -v2], axis=-1)[:2]

    try:
        (t1, t2) = np.linalg.solve(A, d)
    except np.linalg.LinAlgError:
        return float("inf"), float("inf")

    if t1 < 0 or t2 < 0:
        return float("inf"), float("inf")
    return (p1 + t1 * v1)[:2]


rays = []
for line in input_data:
    position, velocity = line.split(" @ ")
    position = np.array(list(map(int, position.split(", "))))
    velocity = np.array(list(map(int, velocity.split(", "))))
    rays.append((position, velocity))

# Q1
result = 0
for ray1, ray2 in tqdm(combinations(rays, 2)):
    x, y = intersection2D(ray1, ray2)
    if (
        x >= test_range[0]
        and x <= test_range[1]
        and y >= test_range[0]
        and y <= test_range[1]
    ):
        result += 1
print(result)


# Q2
def cross(x1, x2, y1, y2, z1, z2):
    return (x1 * y2 - x2 * y1, y1 * z2 - y2 * z1, z1 * x2 - z2 * x1)


x, y, z, vx, vy, vz = symbols("x y z vx vy vz")
equations = []
for r, v in rays[:3]:
    x2, y2, z2 = r
    vx2, vy2, vz2 = v
    equations.extend(cross(x2 - x, vx2 - vx, y2 - y, vy2 - vy, z2 - z, vz2 - vz))

sol = solve(equations, x, y, z, vx, vy, vz)[0]
print(sol[0] + sol[1] + sol[2])
