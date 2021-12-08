with open("input.txt") as f:
    text = [[w.split(" ") for w in line] for line in [line[:-1].split(" | ") for line in f.readlines()]]

output_text = [t[1] for t in text]
output_lengths = [len(t) for row in output_text for t in row]
sum_of_easy_numbers = len(list(filter(lambda n: n in [2, 4, 3, 7], output_lengths)))
print(sum_of_easy_numbers)


normal_correspondance = {0: set("abcefg"),
                         1: set("cf"),
                         2: set("acdeg"),
                         3: set("acdfg"),
                         4: set("bcdf"),
                         5: set("abdfg"),
                         6: set("abdefg"),
                         7: set("acf"),
                         8: set("abcdefg"),
                         9: set("abcdfg")}
wire_presence = {c: sum(c in cset for _, cset in normal_correspondance.items()) for c in "abcdefg"}
print(wire_presence)
def deduce_numbers(input_numbers, output_numbers):
    possible_a_chars = []
    wire_cor = {}
    wire_presence = {c: sum(c in cset for cset in input_numbers) for c in "abcdefg"}
    print(wire_presence)
    for n in input_numbers:
        if len(n) in [2, 3]:
            possible_a_chars.append(set(n))
    p1, p2 = possible_a_chars
    wire_cor["a"] = ((p1 | p2) - (p1 & p2)).pop()
    for c, n in wire_presence.items():
        if n == 6:
            wire_cor['b'] = c
        elif n == 4:
            wire_cor['e'] = c
        elif n == 9:
            wire_cor['f'] = c
        elif n == 8 and c != wire_cor["a"]:
            wire_cor['c'] = c
    output = ''
    for n in output_numbers:
        if len(n) == 2:
            output+='1'
        elif len(n) == 3:
            output+='7'
        elif len(n) == 4:
            output+='4'
        elif len(n) == 7:
            output+='8'
        if len(n) == 5:
            if wire_cor["c"] in n and wire_cor["f"] in n:
                output+='3'
            elif wire_cor["c"] in n:
                output+='2'
            else:
                output+='5'
        elif len(n) == 6:
            if wire_cor["c"] in n and wire_cor["e"] in n:
                output+='0'
            elif wire_cor["c"] in n:
                output+='9'
            else:
                output+='6'
    print(output_numbers, output)
    return int(output)
print(sum(deduce_numbers(*t) for t in text))