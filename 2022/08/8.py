import numpy as np
import matplotlib.pyplot as plt

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

input_data = np.array([list(map(int, line)) for line in input_data])

# Q1
def visible_from_above(data):
    visible = np.full_like(data, False)
    visible[0] = True
    max = np.maximum.accumulate(data)
    visible[1:] |= max[1:] > max[:-1]
    return visible

plt.figure()
plt.imshow(input_data)
plt.colorbar()
visible = visible_from_above(input_data)
visible |= visible_from_above(input_data[::-1])[::-1]
visible |= visible_from_above(input_data.T).T
visible |= visible_from_above(input_data.T[::-1])[::-1].T
print(visible.sum())

plt.figure()
plt.imshow(visible)

# Q2
def visible_along_axis(data):
    view = np.zeros_like(data)
    for i in range(1, data.shape[0] - 1):
        diff = (data[i] - data) > 0
        view[i] = (1 + np.cumprod(diff[i-1:0:-1], axis=0).sum(axis=0)) * (
            1 + np.cumprod(diff[i + 1 :-1], axis=0).sum(axis=0)
        )
    return view


score = visible_along_axis(input_data) * visible_along_axis(input_data.T).T
plt.figure()
plt.imshow(np.log(score))
plt.colorbar()
plt.show()
print(score.max())
