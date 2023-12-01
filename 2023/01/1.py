import regex as re

with open("input.txt") as f:
    input_string = f.read().split("\n")[:-1]

numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
for n in range(1, 10):
    numbers[str(n)] = str(n)

digits = [
    re.findall("|".join(list(numbers)[::-1]), line, overlapped=True)
    for line in input_string
]
print(sum(int(numbers[line[0]] + numbers[line[-1]]) for line in digits))
