import numpy as np

with open("input.txt") as f:
    grid = [list(line) for line in f.read().splitlines()]

grid = np.array(grid, dtype=int)
h, w = grid.shape
fgrid= np.zeros((5*h, 5*w))
for i in range(5):
    for j in range(5):
        fgrid[i*h: (i+1)*h, j*w: (j+1)*w] = np.mod(grid + i + j - 1, 9) + 1
grid = fgrid
big_grid = np.full((grid.shape[0] + 2, grid.shape[1] + 2), fill_value=np.inf)
big_grid[1:-1, 1:-1] = grid
grid = big_grid

def get_links(grid, costs, node):
    i, j = node
    return {node: grid[node] for node in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if costs[node] < 0}
    

costs = np.full_like(grid, -1)
costs[1,1] = 0
visited = {(1, 1)}
i = 0
while costs[-2, -2] < 0:
    best_new_cost = float("inf")
    to_remove = set()
    for n in visited:
        links = get_links(grid, costs, n)
        if len(links) == 0 or min(links.values()) == np.inf:
            to_remove.add(n)
        else:
            for n2, link_cost in links.items():
                new_cost = costs[n] + link_cost
                if (best_new_cost > new_cost):
                    best_new_cost = new_cost
                    best_node = n2
    visited.add(best_node)
    visited -= to_remove
    costs[best_node] = best_new_cost

print(costs[-2, -2])