from functools import reduce

with open("input.txt") as f:
    monkey_data = f.read().split("\n\n")


class Monkey:
    def __init__(self, data: str, monkey_list: list) -> None:
        self.monkey_list = monkey_list
        for i, line in enumerate(data.strip().split("\n")):
            if i == 0:
                self.name = int(line.split()[-1][:-1])
            elif i == 1:
                _, items = line.split(": ")
                self.items = list(map(int, items.split(", ")))
            elif i == 2:
                self.update_fun = eval(f"lambda old: {line.split('new = ')[1]}")
            elif i == 3:
                self.test_div = int(line.split()[-1])
            elif i == 4:
                self.monkey_true = int(line.split()[-1])
            elif i == 5:
                self.monkey_false = int(line.split()[-1])
        self.inspected = 0
    
    def update(self):
        for item in self.items:
            item = self.update_fun(item) % self.super_divider
            if item % self.test_div == 0:
                self.monkey_list[self.monkey_true].items.append(item)
            else:
                self.monkey_list[self.monkey_false].items.append(item)
        self.inspected += len(self.items)
        self.items = []

monkeys = []
for data in monkey_data:
    monkeys.append(Monkey(data, monkeys))
super_divider = reduce(lambda x, y: x*y, [m.test_div for m in monkeys])
for m in monkeys:
    m.super_divider = super_divider
n_steps = 10000
for i in range(n_steps):
    for m in monkeys:
        m.update()

inspected = sorted([m.inspected for m in monkeys])
print(inspected[-1] * inspected[-2])