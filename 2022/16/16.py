from copy import deepcopy
from tqdm import tqdm
import functools

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

graph = {}
for line in input_data:
    line = line.split()
    key = line[1]
    flow = int(line[4].split("=")[1][:-1])
    dest = [l.strip(",") for l in line[9:]]
    graph[key] = {"flow": flow, "dest": {k: 1 for k in dest}}


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


@functools.lru_cache(maxsize=None)
def get_score_Q1(root, visited, remaining):
    total_score = 0
    total_path = [root]
    distances = graph[root]["dest"]
    if remaining > 1:
        scores = {
            p: (remaining - distance - 1) * graph[p]["flow"]
            for p, distance in distances.items()
            if p not in visited
        }
        for dest, score in scores.items():
            candidate_score, path = get_score_Q1(
                dest, visited.union({dest}), remaining - distances[dest] - 1
            )
            if total_score < candidate_score + score:
                total_score = candidate_score + score
                total_path = (root, *path)
    return total_score, total_path


def get_score_Q2(root, visited, remaining):
    total_score = 0
    total_path = [[], []]
    distances = graph[root]["dest"]
    if remaining > 1:
        scores = {
            p: (remaining - distance - 1) * graph[p]["flow"]
            for p, distance in distances.items()
            if p not in visited
        }
        if root == "AA":
            iterator = tqdm(scores.items(), total=len(scores))
        else:
            iterator = scores.items()
        for dest, score in iterator:
            candidate_score, paths = get_score_Q2(
                dest, visited.union({dest}), remaining - distances[dest] - 1
            )
            if total_score < candidate_score + score:
                total_score = candidate_score + score
                total_path = [[root] + paths[0], paths[1]]
        elephant_score, elephant_path = get_score_Q1("AA", visited, 26)
        if total_score < elephant_score:
            total_score = elephant_score
            total_path = [[root], elephant_path]
    return total_score, total_path


print(get_score_Q1("AA", frozenset(["AA"]), 30))
print(get_score_Q2("AA", frozenset(["AA"]), 26))
