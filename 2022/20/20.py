import numpy as np
from copy import copy
from tqdm import tqdm, trange

with open("input.txt") as f:
    input_data = list(map(int, f.read().strip().split()))

Q1 = True
if not Q1:
    key = 811589153
    input_data = [key * d for d in input_data]
n = len(input_data)
indeces = np.arange(n)
if Q1:
    n_fold = 1
else:
    n_fold = 10
for j in trange(n_fold):
    for i, value in enumerate(tqdm(input_data, leave=False)):
        index = indeces[i]
        new_index = (index + value - 1) % (n - 1) + 1
        if new_index > index:
            indeces[(indeces <= new_index) & (indeces > index)] -= 1
        else:
            indeces[(indeces >= new_index) & (indeces < index)] += 1
        indeces[i] = new_index

updated = copy(input_data)
for j, k in enumerate(indeces):
    updated[k] = input_data[j]
zero_index = indeces[input_data.index(0)]
print(
    sum(
        [
            updated[(zero_index + 1000) % n],
            updated[(zero_index + 2000) % n],
            updated[(zero_index + 3000) % n],
        ]
    )
)
