import numpy as np
from tqdm import tqdm

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")

global_max = 0


def score(ore_robot, clay_robot, obsidian_robot, geode_robot, start_budget=24):
    global global_max
    costs = np.array(
        [
            [ore_robot, 0, 0, 0],
            [clay_robot, 0, 0, 0],
            [obsidian_robot[0], obsidian_robot[1], 0, 0],
            [geode_robot[0], 0, geode_robot[1], 0],
        ],
        dtype=int,
    )
    max_costs = costs.max(0)
    start_available_ressources = np.zeros(4, dtype=int)
    start_available_robots = np.zeros(4, dtype=int)
    start_available_robots[0] = 1

    def when_to_build(available_ressources, available_robots):
        needed = costs - available_ressources
        time_remaining = needed / available_robots
        time_remaining[needed <= 0] = 0
        time_remaining = np.ceil(time_remaining.max(1))
        return time_remaining

    global_max = 0

    def get_max_geode(robots, ressources, budget=start_budget):
        global global_max
        if (
            ressources[-1] + robots[-1] * budget + budget * (budget - 1) / 2
            <= global_max
        ):
            return
        if max_costs[0] < robots[0]:
            return
        if max_costs[1] < robots[1]:
            return
        if max_costs[2] < robots[2]:
            return

        robots_np = np.array(robots)
        ressources_np = np.array(ressources)
        for i, time_remaining in enumerate(when_to_build(ressources_np, robots_np)):
            if not np.isfinite(time_remaining) or time_remaining > budget - 1:
                continue
            time_remaining = int(time_remaining) + 1
            new_robots = robots_np.copy()
            new_robots[i] += 1
            get_max_geode(
                robots=tuple(new_robots),
                ressources=tuple(ressources_np + robots_np * time_remaining - costs[i]),
                budget=budget - time_remaining,
            )
        final_max = ressources[-1] + budget * robots[-1]
        global_max = max(global_max, final_max)

    get_max_geode(
        tuple(start_available_robots),
        tuple(start_available_ressources),
        budget=start_budget,
    )

    return global_max


np.seterr(all="ignore")

Q1 = False
# Q1
if Q1:
    qualities = {}
    for line in tqdm(input_data):
        words = line.split()
        id_blueprint = int(words[1][:-1])
        ore = int(words[6])
        clay = int(words[12])
        obsidian = [int(w) for w in [words[18], words[21]]]
        geode = [int(w) for w in [words[27], words[30]]]
        quality = score(ore, clay, obsidian, geode)
        qualities[id_blueprint] = quality
        print(quality)

    print(sum(k * q for k, q in qualities.items()))
else:
    # Q2
    qualities = []
    for line in tqdm(input_data[:3]):
        words = line.split()
        id_blueprint = int(words[1][:-1])
        ore = int(words[6])
        clay = int(words[12])
        obsidian = [int(w) for w in [words[18], words[21]]]
        geode = [int(w) for w in [words[27], words[30]]]
        quality = score(ore, clay, obsidian, geode, start_budget=32)
        qualities.append(quality)
        print(quality)

    print(np.array(qualities).prod())
