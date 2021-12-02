import pandas as pd

a = pd.read_csv("input.txt", header=None, sep=" ", index_col=0, names=["strength"])

# first question
print(a.loc["forward"].sum() * (a.loc["down"].sum() - a.loc["up"].sum()))

# second question
a["aim"] = (a["strength"] * (a.index == "down")).cumsum()
a["aim"] -= (a["strength"] * (a.index == "up")).cumsum()

print(a.loc["forward"].prod(axis=1).sum() * a.loc["forward", "strength"].sum())