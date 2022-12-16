from copy import deepcopy
from tqdm import tqdm

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

graph = {}
for line in input_data:
    line = line.split()
    key = line[1]
    flow = int(line[4].split("=")[1][:-1])
    dest = [l.strip(",") for l in line[9:]]
    graph[key] = {"flow": flow, "dest": {k : 1 for k in dest}}


complete_graph = {}
def bfs(key):
    queue = [key]
    explored = []
    complete_graph[key] = deepcopy(graph[key])
    while queue:
        k = queue.pop(0)
        explored.append(k)
        node = graph[k]
        for j in node["dest"]:
            if j in explored:
                continue
            else:
                if k != key:
                    complete_graph[key]["dest"][j] = 1 + complete_graph[key]["dest"][k]
                queue.append(j)

for key in graph:
    bfs(key)

graph = complete_graph

original_keys = sorted(list(graph.keys()))
first = "AA"

for k in original_keys[1:]:
    node = graph[k]
    if node["flow"] == 0:
        graph.pop(k)
        for i in graph:
            graph[i]["dest"].pop(k, None)

print(graph)

def get_score_Q1(root, visited, remaining):
    total_score = 0
    total_path = [root]
    distances = graph[root]["dest"]
    if remaining > 1:
        scores = {p: (remaining-distance-1) * graph[p]["flow"] for p, distance in distances.items() if p not in visited}
        for dest, score in scores.items():
            candidate_score, path = get_score_Q1(dest, visited + [dest], remaining - distances[dest] - 1)
            if total_score < candidate_score + score:
                total_score = candidate_score + score
                total_path = [root] + path
    return total_score, total_path

def get_score_Q2(root1, root2, visited, remaining1, remaining2):
    total_score = 0
    swapped = False
    if remaining1 < remaining2:
        root1, root2 = root2, root1
        remaining1, remaining2 = remaining2, remaining1
        swapped = True
    
    distances = graph[root1]["dest"]
    total_path = [[root1], [root2]]
    if remaining1 > 1:
        scores = {p: (remaining1-distance-1) * graph[p]["flow"] for p, distance in distances.items() if p not in visited}
        if root1 == "AA":
            iterator = tqdm(scores.items(), total=len(scores))
        else:
            iterator = scores.items()
        for dest, score in iterator:
            candidate_score, path = get_score_Q2(dest, root2, visited + [dest], remaining1 - distances[dest] - 1, remaining2)
            if total_score < candidate_score + score:
                total_score = candidate_score + score
                if swapped:
                    total_path = [path[1], [root1] + path[0]]
                else:
                    total_path = [[root1] + path[0], path[1]]
                
    return total_score, total_path

print(get_score_Q1(first, [first], 30))
print(get_score_Q2(first, first, [first], 26, 26))

