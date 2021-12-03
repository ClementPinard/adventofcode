import pandas as pd

def invert(bitstr):
    return map(lambda x: '0' if x == '1' else '1', bitstr)

with open("input.txt") as f:
    array = f.readlines()

#Q1    
df = pd.DataFrame([list(row[:-1]) for row in array]).astype(int)
most_frequent = df.mode().iloc[0]
gamma_string = ''.join(most_frequent.values.astype(str))
gamma = int(gamma_string, 2)
epsilon_string = ''.join(invert(gamma_string))
epsilon = int(epsilon_string, 2)
print(gamma, epsilon, gamma * epsilon)

#Q2
def get_sequence(df, get_most_frequent=True):
    n_candidates = df.shape[1]
    df_filtered = df
    col = 0
    while(n_candidates > 1):
        counts = df_filtered[col].value_counts()
        if counts[0] == counts[1]:
            most_frequent = 1
        else:
            most_frequent = counts.index[0]
        if get_most_frequent:
            target = most_frequent
        else:
            target = 1 - most_frequent
        candidates = df_filtered[col] == target
        col += 1
        df_filtered = df_filtered[candidates]
        n_candidates = candidates.sum()
    return ''.join(df_filtered.iloc[0].astype(str))
    
ox = int(''.join(get_sequence(df)), 2)
co2 = int(''.join(get_sequence(df, get_most_frequent=False)), 2)
print(ox, co2, ox*co2)