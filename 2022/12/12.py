import numpy as np
from tqdm import tqdm

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

input_data = np.array([list(map(ord, line)) for line in input_data])
H, W = input_data.shape

startx, starty = np.nonzero(input_data == ord("S"))
startx, starty = startx[0], starty[0]
endx, endy = np.nonzero(input_data == ord("E"))
endx, endy = endx[0], endy[0]
input_data[startx, starty] = ord("a")
input_data[endx, endy] = ord("z")
input_data -= ord('a')
n_candidate = (input_data == 0).sum()

def get_score(startx, starty, plot=True):
    scores = np.full_like(input_data, np.inf, dtype=float)
    scores[startx, starty] = 0
    open_set = {(startx, starty)}
    closed_set = set()
    def add(pos1, pos2):
        candidate_score = scores[pos1[0], pos1[1]] + 1
        score = scores[pos2[0], pos2[1]]
        if pos2 in closed_set and score <= candidate_score:
            return
        scores[pos2[0], pos2[1]] = candidate_score
        open_set.add(pos2)

    while np.isinf(scores[endx, endy]) and open_set:
        x, y = sorted(open_set, key=lambda pos: scores[pos[0], pos[1]])[0]
        open_set.remove((x,y))
        if x > 0 and (input_data[x - 1, y] - input_data[x, y]) <= 1:
            add((x,y), (x-1, y))
        if x < H - 1 and (input_data[x + 1, y] - input_data[x, y]) <= 1:
            add((x,y), (x+1, y))
        if y > 0 and (input_data[x, y - 1] - input_data[x, y]) <= 1:
            add((x,y), (x, y-1))
        if y < W - 1 and (input_data[x, y + 1] - input_data[x, y]) <= 1:
            add((x,y), (x, y+1))
        closed_set.add((x, y))
    if plot:
        import matplotlib.pyplot as plt
        plt.imshow(scores)
        plt.show()
    return scores[endx, endy]

#Q1
print(int(get_score(startx, starty)))

#Q2
lowest_score = np.inf
for startx, starty in tqdm(zip(*np.where(input_data == 0)), total=n_candidate):
    lowest_score = min(lowest_score, get_score(startx, starty, plot=False))
print(int(lowest_score))