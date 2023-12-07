from collections import Counter

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

# input_data = """32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483""".split("\n")

# Q1
card_values = {c: i for i, c in enumerate("AKQJT98765432"[::-1])}

data = []
for line in input_data:
    hand, bid = line.split()
    current_card_values = [card_values[c] for c in hand]
    hand = Counter(hand)
    bid = int(bid)
    most_common = hand.most_common(2)
    first = most_common[0]
    if len(most_common) == 2:
        second = most_common[1]
    else:
        second = (0, 0)
    if first[1] == 5:
        hand_value = 6
    elif first[1] == 4:
        hand_value = 5
    elif first[1] == 3:
        if second[1] == 2:
            hand_value = 4
        else:
            hand_value = 3
    elif first[1] == 2:
        if second[1] == 2:
            hand_value = 2
        else:
            hand_value = 1
    else:
        hand_value = 0
    data.append([[hand_value, *current_card_values], bid])

score = sum((i + 1) * c[1] for i, c in enumerate(sorted(data, key=lambda x: x[0])))
print(score)

# Q2
card_values = {c: i for i, c in enumerate("AKQT98765432J"[::-1])}
data = []
for line in input_data:
    hand, bid = line.split()
    current_card_values = [card_values[c] for c in hand]
    hand = Counter(hand)
    bid = int(bid)
    most_common = hand.most_common(2)
    first = most_common[0]
    if first[0] == "J" and len(most_common) == 2:
        hand[most_common[1][0]] += hand["J"]
        hand["J"] = 0
        most_common = hand.most_common(2)
    if first[0] != "J" and "J" in hand:
        hand[first[0]] += hand["J"]
        hand["J"] = 0
        most_common = hand.most_common(2)
    first = most_common[0]
    if len(most_common) == 2:
        second = most_common[1]
    else:
        second = (0, 0)

    if first[1] == 5:
        hand_value = 6
    elif first[1] == 4:
        hand_value = 5
    elif first[1] == 3:
        if second[1] == 2:
            hand_value = 4
        else:
            hand_value = 3
    elif first[1] == 2:
        if second[1] == 2:
            hand_value = 2
        else:
            hand_value = 1
    else:
        hand_value = 0
    data.append([[hand_value, *current_card_values], bid])

score = sum((i + 1) * c[1] for i, c in enumerate(sorted(data, key=lambda x: x[0])))
print(score)
