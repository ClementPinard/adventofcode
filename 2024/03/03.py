with open("input.txt") as f:
    input_string = f.read()[:-1]


def parse_muls(string: str):
    result = 0
    for substring in string.split("mul("):
        if ")" not in substring:
            continue
        inside = substring.split(")")[0]
        if "," not in inside:
            continue
        try:
            left, right = inside.split(",")
        except ValueError:
            continue
        try:
            result += int(left) * int(right)
        except ValueError:
            pass
    return result


# Q1
print(parse_muls(input_string))

# Q2
positive_strings = input_string.split("do()")
result = 0
for positive_substring in positive_strings:
    result += parse_muls(positive_substring.split("don't()")[0])
print(result)
