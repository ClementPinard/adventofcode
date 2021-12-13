from collections import defaultdict

with open("input.txt") as f:
    links = [line.split("-") for line in f.read().splitlines()]

forward_links = defaultdict(list)
for i1, i2 in links:
    forward_links[i1].append(i2)
    forward_links[i2].append(i1)

big_caves = [k for k in forward_links if k.upper() == k]

def find_paths(node, visited, visited_twice):
    npaths = 0
    for next_node in forward_links[node]:
        if next_node == "start":
            continue
        elif next_node == "end":
            npaths += 1
        elif (next_node not in big_caves) and (next_node in visited):
            if visited_twice:
                continue
            else:
                npaths += find_paths(next_node, visited + [next_node], True)
        else:
            npaths += find_paths(next_node, visited + [next_node], visited_twice)
    return npaths


print(find_paths("start", ["start"], False))