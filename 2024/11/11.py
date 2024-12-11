from tqdm import trange
from collections import Counter, defaultdict

with open("input.txt") as f:
    input_data = f.read().strip().split()


def blink(number):
    if len(number) % 2 == 0:
        return number[: len(number) // 2], str(int(number[len(number) // 2 :]))
    elif number == "0":
        return ["1"]
    else:
        return [str(int(number) * 2024)]


result_sum = 0
counter = Counter(input_data)
for _ in trange(75):
    last_counter, counter = counter, defaultdict(int)
    for number in input_data:
        for n in blink(number):
            counter[n] += last_counter[number]
    input_data = counter.keys()

print(sum(counter.values()))
