import pandas as pd
input_data = pd.read_csv("input.txt", header=None, sep=' ').replace({0:{"A": 0, "B": 1, "C": 2}, 1:{"X": 0, "Y": 1, "Z": 2}})
opp, you = input_data[0], input_data[1]


#Q1
won = you == (opp + 1).mod(3)
draw = you == opp

score = (you + 1).sum() + 6 * won.sum() + 3 * draw.sum()
print(score)

#Q2

won = you == 2
draw = you == 1
lost = you == 0
you = (opp + 1) * won + opp * draw + (opp - 1) * lost
you = you.mod(3)
score = (you + 1).sum() + 6 * won.sum() + 3 * draw.sum()
print(score)