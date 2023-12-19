from copy import copy

input_data = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".split("\n\n")

with open("input.txt") as f:
    input_data = f.read().split("\n\n")

workflows, parts = input_data
workflows = input_data[0].split("\n")
parts = input_data[1].split("\n")[:-1]

workflow_dict = {}
for w in workflows:
    name, instructions = w.split("{")
    instructions_list = instructions[:-1].split(",")
    current_workflow = {"last": instructions_list[-1], "ins": []}
    for ins in instructions_list[:-1]:
        i, dest = ins.split(":")
        if ">" in i:
            key, value = i.split(">")
            comp = ">"
        else:
            key, value = i.split("<")
            comp = "<"
        current_workflow["ins"].append((key, int(value), comp, dest))
    workflow_dict[name] = current_workflow

# Q1

parts_list = []
for p in parts:
    stats = p[1:-1].split(",")
    current_part = {}
    for s in stats:
        name, value = s.split("=")
        current_part[name] = int(value)
    parts_list.append(current_part)

final_dest = {"A": [], "R": []}
for part in parts_list:
    current_workflow = workflow_dict["in"]
    while True:
        destination = current_workflow["last"]
        for key, value, comp, dest in current_workflow["ins"]:
            match comp:
                case ">":
                    if part[key] > value:
                        destination = dest
                        break
                case "<":
                    if part[key] < value:
                        destination = dest
                        break
        if destination in "AR":
            final_dest[destination].append(part)
            break
        else:
            current_workflow = workflow_dict[destination]

result = 0
for part in final_dest["A"]:
    result += sum(part.values())
print(result)

# Q2
parts = [("in", {k: (1, 4000) for k in "xmas"})]
final_dest = []
while parts:
    workflow_name, part_range = parts.pop(0)
    if workflow_name in "AR":
        if workflow_name == "A":
            final_dest.append(part_range)
        continue
    current_workflow = workflow_dict[workflow_name]
    for key, value, comp, dest in current_workflow["ins"]:
        vmin, vmax = part_range[key]
        match comp:
            case ">":
                if vmax <= value:
                    continue
                new_part_range = copy(part_range)

                new_part_range[key] = (max(vmin, value + 1), vmax)
                parts.append((dest, new_part_range))
                part_range[key] = (vmin, value)
            case "<":
                if vmin >= value:
                    continue
                new_part_range = copy(part_range)
                new_part_range[key] = (vmin, min(vmax, value - 1))
                parts.append((dest, new_part_range))
                part_range[key] = (value, vmax)
    parts.append((current_workflow["last"], part_range))

result = 0
for r in final_dest:
    volume = 1
    for vmin, vmax in r.values():
        volume *= vmax - vmin + 1
    result += volume
print(result)
