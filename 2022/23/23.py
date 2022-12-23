import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

with open("input2.txt") as f:
    input_data = f.read().strip().split("\n")


class Elf:
    def __init__(self, i, position) -> None:
        self.i = i
        self.position = position
        self.directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]).T
        self.ortho_directions = self.directions[[1, 0]]
        self.considered_directions = np.arange(4, dtype=int)

    def propose(self, positions):
        differences = positions - self.position
        candidate = np.abs(differences).max(1) <= 1
        candidate[self.i] = False
        if True not in candidate:
            self.future_position = self.position
            return False
        differences = differences[candidate]
        colinear = differences @ self.directions
        ortho = differences @ self.ortho_directions
        invalid = ((colinear == 1) & (np.abs(ortho) <= 1)).max(0)
        if False not in invalid:
            self.future_position = self.position
            return False
        self.future_position = (
            self.position
            + self.directions[
                :,
                self.considered_directions[
                    invalid[self.considered_directions].argmin()
                ],
            ]
        )
        return True

    def maybe_move(self, other_propositions):
        same_position = ((other_propositions - self.future_position) == 0).all(1)
        same_position[self.i] = False
        if same_position.any():
            return
        self.position = self.future_position

    def finish_turn(self):
        self.considered_directions = self.considered_directions[[1, 2, 3, 0]]


elves_coords = []
for i, line in enumerate(input_data):
    for j, char in enumerate(line):
        if char == "#":
            elves_coords.append([i, j])

elves_coords = np.array(elves_coords)
elves_coords2 = np.copy(elves_coords)
print("\n".join(input_data))
print(elves_coords)

arange = np.arange(len(elves_coords))

def propose_elf(elves_coords, directions):
    ortho_directions = directions[[1, 0]]
    differences = elves_coords - elves_coords[:, None]
    differences[arange, arange] = 2
    colinear = differences @ directions
    ortho = differences @ ortho_directions
    invalid = ((colinear == 1) & (np.abs(ortho) <= 1))
    invalid = invalid.any(1)
    cant_move = invalid.all(1) | ~invalid.any(1)
    move = np.where(cant_move[:, None], 0, directions.T[invalid.argmin(1)])
    return elves_coords + move, move.max()

def maybe_move(elves_coords, elves_propositions):
    differences = elves_propositions - elves_propositions[:, None]
    differences[arange, arange] = 1
    same_position = (differences == 0).all(axis=2).any(1)
    return np.where(same_position[:, None], elves_coords, elves_propositions)

def plot_elves(elves_coords):
    normalized_elves_coords = elves_coords - elves_coords.min(0)
    h, w = normalized_elves_coords.max(0)
    canvas = np.zeros((h + 1, w + 1))
    canvas[normalized_elves_coords[:, 0], normalized_elves_coords[:, 1]] = 2 + np.arange(
        len(elves)
    )
    print((canvas == 0).sum())
    plt.imshow(canvas)
    plt.show()
    

directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]).T
ortho_directions = directions[[1, 0]]

elves = [Elf(i, c) for i, c in enumerate(elves_coords)]
step = 0
progress = tqdm()
while any(can_move := list(e.propose(elves_coords) for e in elves)):
    step += 1
    progress.update(1)
    elves_propositions = np.stack(list(e.future_position for e in elves))
    for e, c in zip(elves, can_move):
        if c:
            e.maybe_move(elves_propositions)
        e.finish_turn()
    elves_coords = np.stack(list(e.position for e in elves))
    if step % 100 == 0:
        plot_elves(elves_coords)

progress.close()
plot_elves(elves_coords)
elves_coords = elves_coords2
move = True
progress = tqdm()
while move:
    progress.update(1)
    propositions, move = propose_elf(elves_coords, directions)
    elves_coords = maybe_move(elves_coords, propositions)
    directions=directions[:,[1,2,3,0]]
progress.close()
plot_elves(elves_coords)
