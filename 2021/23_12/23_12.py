import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)
from tqdm import trange

positions = [["C", "D"], ["C", "A"], ["B", "B"], ["D", "A"]]
#positions = [["B", "A"],["C", "D"],["B", "C"], ["D", "A"]]
moved = [[False, False], [False, False], [False, False], [False, False]]
letter_pos = [[0, 0, -1], [0,1,-1],
              [1, 0, -1], [1,1,-1],
              [2, 0, -1], [2,1,-1],
              [3, 0, -1], [3,1,-1]]
hallway = [None] * 7

points = {"A":1, "B":10, "C":100, "D":1000}

costs = {(0,0):3, (1,0):2, (2,0):2, (3,0):4, (4,0):6, (5,0):8, (6,0):9,
         (0,1):5, (1,1):4, (2,1):2, (3,1):2, (4,1):4, (5,1):6, (6,1):7,
         (0,2):7, (1,2):6, (2,2):4, (3,2):2, (4,2):2, (5,2):4, (6,2):5,
         (0,3):9, (1,3):8, (2,3):6, (3,3):4, (4,3):2, (5,3):2, (6,3):3,}

paths = {(0,0):[1], (1,0):[], (2,0):[], (3,0):[2], (4,0):[2,3], (5,0):[2,3,4], (6,0):[2,3,4,5],
         (0,1):[1,2], (1,1):[2], (2,1):[], (3,1):[], (4,1):[3], (5,1):[3,4], (6,1):[3,4,5],
         (0,2):[1,2,3], (1,2):[2,3], (2,2):[3], (3,2):[], (4,2):[], (5,2):[4], (6,2):[4,5],
         (0,3):[1,2,3,4], (1,3):[2,3,4], (2,3):[3,4], (3,3):[1], (4,3):[], (5,3):[], (6,3):[5]}

right_room = {"A":0, "B":1, "C":2, "D":3}


def move(positions, hallway, moved, i,j,k, forward=True, back=False):
    if forward:
        assert positions[i][j] is not None
        assert hallway[k] is None
        letter = positions[i][j]
    else:
        assert positions[i][j] is None
        assert hallway[k] is not None
        letter = hallway[k]
    base_point = points[letter]
    cost = base_point * (costs[(k,i)] + j)
    if j == 1:
        assert positions[i][0] is None
    assert(all(hallway[l] is None for l in paths[(k,i)]))
    
    if not back:
        if forward:
            assert not moved[i][j] or (i != right_room[letter])
        else:
            assert (i == right_room[letter])
            if j==0:
                assert positions[i][1] is not None and i == right_room[positions[i][1]]
        
    
    if forward:
        hallway[k] = positions[i][j]
        positions[i][j] = None
    else:
        positions[i][j] = hallway[k]
        moved[i][j] = not back
        hallway[k] = None
    return cost

def check(positions):
    return positions == [["A", "A"], ["B", "B"], ["C", "C"], ["D", "D"]]

total_costs = []
min_cost = float("inf")
current_cost = 0
def search(positions, hallway, moved, current_cost, first=False):
    global min_cost
    print(positions, hallway)
    if current_cost >= min_cost:
        return
    if check(positions):
        total_costs.append(current_cost)
        if min_cost > current_cost:
            print(current_cost)
            min_cost = current_cost
        return
    for i in (trange(4) if first else range(4)):
        for j in range(2):
            for k in trange(7) if first else range(7):
                for l in range(2):
                    try:
                        new_cost = current_cost + move(positions, hallway, moved, i,j,k,l==0)
                        search(positions, hallway, moved, new_cost)
                        move(positions, hallway, moved, i,j,k,l==1, back=True)
                        
                    except AssertionError as e:
                        pass

search(positions, hallway, moved, 0, True)
print(total_costs)
print(min(total_costs))