from collections import defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()

sequence = lines[0]
mutations = {}
for line in lines[2:]:
    pair, c = line.split(" -> ")
    mutations[pair] = c

pair_occurences = defaultdict(int)
for c1, c2 in zip(sequence, sequence[1:]):
    pair_occurences[c1+c2] += 1
n_iter = 40
for i in range(n_iter):
    new_occurences = defaultdict(int)
    for (c1, c2), n in pair_occurences.items():
        c3 = mutations[c1+c2]
        new_occurences[c1+c3] += n
        new_occurences[c3+c2] += n
    pair_occurences = new_occurences
c_occurences = {c: sum(pair_occurences[k] for k in pair_occurences if k[0] == c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXZ'}
c_occurences = {k: v for k, v in c_occurences.items() if v>0}
c_occurences[sequence[-1]] += 1
c_occurences = sorted(c_occurences.values())
print(c_occurences[-1] - c_occurences[0])