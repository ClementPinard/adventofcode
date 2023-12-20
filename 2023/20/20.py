from collections import defaultdict
from tqdm import trange
from copy import copy
import numpy as np

input_data = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

fliflops = {}
cons = {}
inputs = defaultdict(set)
signals = []

for line in input_data:
    module, destination = line.split(" -> ")
    destination = destination.split(", ")
    match module[0]:
        case "&":
            cons[module[1:]] = [{}, destination]
        case "%":
            fliflops[module[1:]] = [False, destination]
        case _:
            signals.extend([[False, d, module] for d in destination])
    for d in destination:
        inputs[d].add(module[1:])

for name, con in cons.items():
    con[0] = {k: False for k in inputs[name]}
outputs = []

bb_periods = {k: [] for k in cons["bb"][0]}
print(bb_periods)
for n_press in trange(10000):
    signals_ = copy(signals)
    outputs.append(False)
    outputs.extend([s[0] for s in signals_])
    rx = 0
    while signals_:
        height, module, origin = signals_.pop(0)
        if module in fliflops:
            f_height, dest = fliflops[module]
            if not height:
                f_height = not f_height
                fliflops[module][0] = f_height
                signals_.extend([f_height, d, module] for d in dest)
                outputs.extend([f_height] * len(dest))
        elif module in cons:
            input_dict, dest = cons[module]
            input_dict[origin] = height
            output_height = not all(input_dict.values())
            signals_.extend([output_height, d, module] for d in dest)
            outputs.extend([output_height] * len(dest))
            if module == "bb" and True in input_dict.values():
                for k, v in input_dict.items():
                    if v:
                        bb_periods[k].append(n_press + 1)

outputs = np.array(outputs)
print(outputs.sum())
print((~outputs).sum())
print(outputs.sum() * (~outputs).sum())
# Encore les restes chinois, sauf que les restes sont à 0, donc lcm des premieres
# valeurs tout simplement
print(np.lcm.reduce([a[0] for a in bb_periods.values()]))
