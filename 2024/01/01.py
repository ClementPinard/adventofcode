import pandas as pd
import numpy as np

a = pd.read_csv("input.txt", sep="   ", header=None)
# Q1
print(
    (
        a[1].sort_values().reset_index(drop=True)
        - a[0].sort_values().reset_index(drop=True)
    )
    .abs()
    .sum()
)

# Q2
print(
    a[1]
    .value_counts()
    .reindex(a[0].unique())
    .fillna(0)
    .astype(int)
    .loc[a[0]]
    .reset_index()
    .prod(axis=1)
    .sum()
)
