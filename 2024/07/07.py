from tqdm import tqdm
from itertools import product

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

total_result = 0
for line in tqdm(input_data):
    result, numbers = line.split(": ")
    result = int(result)
    numbers = list(map(int, numbers.split()))
    for opt_list in product(*[["+", "*", "||"]] * (len(numbers) - 1)):
        sub_result = numbers[0]
        for opt, number in zip(opt_list, numbers[1:]):
            if opt == "+":
                sub_result += number
            elif opt == "*":
                sub_result *= number
            elif opt == "||":
                sub_result = int(f"{sub_result}{number}")
        if sub_result >= result:
            if sub_result == result:
                total_result += result
            break
print(total_result)
