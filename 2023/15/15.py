from collections import defaultdict

with open("input.txt") as f:
    input_data = f.read()[:-1]

# input_data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

# Q1
result = 0
boxes = defaultdict(list)
for sub in input_data.split(","):
    code = 0
    for c in sub:
        code += ord(c)
        code = (17 * code) % 256
    result += code

print(result)


# Q2
result = 0
boxes = defaultdict(list)
focuses = defaultdict(dict)
for sub in input_data.split(","):
    if sub[-1] == "-":
        op = 1
        sub = sub[:-1]
    else:
        op = 2
        sub, focus = sub.split("=")
        focus = int(focus)

    code = 0
    for c in sub:
        code += ord(c)
        code = (17 * code) % 256

    if op == 1:
        if sub in boxes[code]:
            boxes[code].remove(sub)
    else:
        focuses[code][sub] = focus
        if sub not in boxes[code]:
            boxes[code].append(sub)

result = 0
for i, labels in boxes.items():
    for j, l in enumerate(labels):
        result += (i + 1) * (j + 1) * focuses[i][l]
print(boxes)
print(focuses)
print(result)
