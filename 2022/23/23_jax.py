import jax
import jax.numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
use_gpu = True
if use_gpu:
    jax.config.update('jax_platform_name', 'gpu')
else:
    jax.config.update('jax_platform_name', 'cpu')

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

elves_coords = []
for i, line in enumerate(input_data):
    for j, char in enumerate(line):
        if char == "#":
            elves_coords.append([i, j])

elves_coords = np.array(elves_coords)
print("\n".join(input_data))

arange = np.arange(len(elves_coords))


@jax.jit
def propose_elf(elves_coords, directions):
    ortho_directions = directions[np.array([1, 0])]
    differences = elves_coords - elves_coords[:, None]
    # differences[arange, arange] = 2
    differences = differences.at[arange, arange].set(2)
    colinear = differences @ directions
    ortho = differences @ ortho_directions
    invalid = (colinear == 1) & (np.abs(ortho) <= 1)
    invalid = invalid.any(1)
    cant_move = invalid.all(1) | ~invalid.any(1)
    move = np.where(cant_move[:, None], 0, directions.T[invalid.argmin(1)])
    return elves_coords + move, move.max()

@jax.jit
def maybe_move(elves_coords, elves_propositions):
    differences = elves_propositions - elves_propositions[:, None]
    #differences[arange, arange] = 1
    differences = differences.at[arange, arange].set(1)
    same_position = (differences == 0).all(axis=2).any(1)
    return np.where(same_position[:, None], elves_coords, elves_propositions)

def plot_elves(elves_coords):
    normalized_elves_coords = elves_coords - elves_coords.min(0)
    h, w = normalized_elves_coords.max(0)
    canvas = np.zeros((h + 1, w + 1))
    canvas = canvas.at[
        normalized_elves_coords[:, 0], normalized_elves_coords[:, 1]
    ].set(2 + np.arange(elves_coords.shape[0]))
    print((canvas == 0).sum())
    plt.imshow(canvas)
    plt.show()


directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]).T
move = True
progress = tqdm()
while move:
    progress.update(1)
    propositions, move = propose_elf(elves_coords, directions)
    elves_coords, directions = (
        maybe_move(elves_coords, propositions),
        directions[:, [1, 2, 3, 0]],
    )
progress.close()
plot_elves(elves_coords)