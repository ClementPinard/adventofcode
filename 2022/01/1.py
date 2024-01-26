import pandas as pd

with open("input.txt") as f:
    input_data = f.read().split("\n\n")[:-1]

scores = pd.Series([sum(map(int, elf.split("\n"))) for elf in input_data])

print(scores.nlargest(3).sum())
