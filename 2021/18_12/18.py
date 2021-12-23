from copy import deepcopy
from functools import reduce

with open("input.txt") as f:
    sfs = f.read().splitlines()

fishes = []
for line in sfs:
    fishes.append(eval(line))
print(fishes)

def explode(fish, depth=0):
    a, b = fish
    islist = [type(a) == list, type(b) == list]
    if islist[0]:
        if depth==3:
            if islist[1]:
                add_most(b, a[1], "left")
            else:
                fish[1] += a[1]
            fish[0] = 0
            return a[0], "left"
        else:
            v, d = explode(a, depth+1)
            if d == "right":
                if islist[1]:
                    add_most(b, v, "left")
                else:
                    fish[1] += v
                return None, "done"
            elif d == "left":
                return v, d
            elif d == "done":
                return None, "done"
    if islist[1]:
        if depth == 3:
            if islist[0]:
                add_most(a, b[0], "right")
            else:
                fish[0] += b[0]
            fish[1] = 0
            return b[1], "right"
        else:
            v, d = explode(b, depth+1)
            if d == "left":
                if islist[0]:
                    add_most(a, v, "right")
                else:
                    fish[0] += v
                return None, "done"
            elif d == "right":
                return v, d
            elif d == "done":
                return None, "done"
    return None, None

def split(fish):
    a, b = fish
    if type(a) == list:
        if split(a):
            return True
    elif a > 9:
        fish[0] = [a//2, a - a//2]
        return True
    if type(b) == list:
        if split(b):
            return True
    elif b > 9:
        fish[1] = [b//2, b - b//2]
        return True
    return False
    
def add_most(fish, value, direction):
    d = 0 if direction == "left" else 1
    if type(fish[d]) == int:
        fish[d] += value
    else:
        add_most(fish[d], value, direction)

def reducef(fish):
    while True:
        _, done = explode(fish)
        if done is not None:
            continue
        done = split(fish)
        if not done:
            break
    return fish

def add(fish1, fish2):
    return reducef([fish1, fish2])

def magnitude(fish):
    a,b = fish
    if type(a) == list:
        v1 = magnitude(a)
    else:
        v1 = a
    if type(b) == list:
        v2 = magnitude(b)
    else:
        v2 = b
    return 3*v1 + 2*v2

print(magnitude(reduce(add, deepcopy(fishes))))

max_mag = 0
for x in fishes:
    for y in fishes:
        if x == y:
            continue
        max_mag = max(max_mag, magnitude(add(deepcopy(x), deepcopy(y))))
print(max_mag)
