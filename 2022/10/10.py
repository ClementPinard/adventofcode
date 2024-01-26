import pandas as pd

input_data = pd.read_csv("input.txt", header=None, sep=" ")

input_data["cycles"] = input_data[0].replace({"noop": 1, "addx": 2}).cumsum() + 1
input_data["X"] = input_data[1].fillna(0).cumsum() + 1

input_data = input_data.set_index("cycles").reindex(range(1, input_data["cycles"].max()), method="ffill")
input_data["X"] = input_data["X"].fillna(1)
input_data["score"] = input_data.index * input_data["X"]
print(input_data.loc[[20, 60, 100, 140, 180, 220], "score"].sum())

input_data["draw"] = ((input_data.index - 1) % 40 - input_data["X"]).abs() <= 1
array = input_data["draw"].values.astype(int).reshape((-1, 40))
import matplotlib.pyplot as plt
plt.imshow(array)
plt.show()