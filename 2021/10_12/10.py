from functools import reduce
with open("input.txt") as f:
    rows  = f.read().splitlines()

scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
scores_complete = {')': 1, ']': 2, '}': 3, '>': 4}
openclose = {'{': '}', '(': ')', '[': ']', '<': '>'}

faulty = []
remaining = []
for r in rows:
    open_brackets = []
    illegal = False
    for c in r:
        if c in '{[(<':
            open_brackets.append(c)
        elif c in '}])>':
            if openclose[open_brackets[-1]] == c:
                open_brackets.pop()
            else:
                illegal = True
                faulty.append(c)
                break
    if not illegal:
        remaining.append([openclose[c] for c in open_brackets][::-1])
print(sum(scores[c] for c in faulty))
autocomplete_scores = sorted([reduce(lambda x,y: 5*x + scores_complete[y], [0] + r) for r in remaining])
print(autocomplete_scores[len(autocomplete_scores) // 2])
