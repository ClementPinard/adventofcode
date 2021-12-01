import pandas as pd

a = pd.read_csv("input.txt", header=None)

diff = a.diff() > 0

# print(a.diff(), diff, diff.sum())

a3 = a.rolling(3).sum()

print((a3.diff() > 0).sum())