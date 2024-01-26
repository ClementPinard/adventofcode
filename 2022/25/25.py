with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

snafu_chars = {"=": -2, "-": -1, "0": 0, "1": 1, "2":2}
snafu_nb = {0: "0", 1: "1", 2: "2", -1: "-", -2: "="}

def from_snafu(line):
    number = 0
    for i, char in enumerate(line):
        number = 5*number + snafu_chars[char]
    
    return number

number = sum(from_snafu(line) for line in input_data)
print(number)

def to_snafu(number):
    pos = 5
    digits = []
    while number > 0:
        digits.append(number % pos)
        number = number // pos
    digits = [*digits, 0]
    for i in range(len(digits) -1):
        d = digits[i]
        if d > 2:
            digits[i] = d - 5
            digits[i + 1] += 1
    return ''.join(snafu_nb[d] for d in digits[::-1])

print(to_snafu(number))
        
        