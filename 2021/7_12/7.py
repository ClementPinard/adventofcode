import numpy as np

crabs = np.fromfile("input.txt", sep=",", dtype=int)

fuel_lookup = np.cumsum(np.arange(crabs.max() + 1))
fuel = fuel_lookup[crabs].sum()
for n in range(crabs.max()):
    fuel = min(fuel, fuel_lookup[np.abs(crabs - n)].sum())
print(fuel)