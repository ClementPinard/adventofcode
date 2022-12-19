import numpy as np
from functools import lru_cache
from tqdm import tqdm
from collections import defaultdict

with open("input.txt") as f:
    input_data = f.read().strip().split("\n")


def score(ore_robot, clay_robot, obsidian_robot, geode_robot, start_budget=24):
    costs = np.array(
        [
            [ore_robot, 0, 0],
            [clay_robot, 0, 0],
            [obsidian_robot[0], obsidian_robot[1], 0],
            [geode_robot[0], 0, geode_robot[1]],
        ],
        dtype=int,
    )

    start_available_ressources = np.zeros(3, dtype=int)
    start_available_robots = np.zeros(4, dtype=int)
    start_available_robots[0] = 1

    @lru_cache(maxsize=None)
    def when_to_build(available_ressources, available_robots):
        needed = costs - available_ressources
        time_remaining = needed / available_robots[:3]
        time_remaining[needed <= 0] = 0
        time_remaining = np.ceil(time_remaining.max(1))
        return time_remaining

    @lru_cache(maxsize=None)
    def get_max_geode(available_robots, available_ressources, budget=24):
        available_robots_np = np.array(available_robots)
        available_ressources_np = np.array(available_ressources)
        if budget == 1:
            return available_robots[3]
        final_score = 0
        for i, time_remaining in enumerate(
            when_to_build(available_ressources, available_robots)
        ):
            if not np.isfinite(time_remaining) or time_remaining >= budget - 1:
                continue
            time_remaining = int(time_remaining) + 1
            new_robots = available_robots_np.copy()
            new_robots[i] += 1
            final_score = max(
                final_score,
                time_remaining * available_robots[3]
                + get_max_geode(
                    available_robots=tuple(new_robots),
                    available_ressources=tuple(
                        available_ressources_np
                        + available_robots_np[:3] * time_remaining
                        - costs[i]
                    ),
                    budget=budget - time_remaining,
                ),
            )
        final_score = max(final_score, budget * available_robots[3])
        return final_score

    return get_max_geode(
        tuple(start_available_robots), tuple(start_available_ressources), budget=start_budget
    )


np.seterr(all="ignore")

Q1 = False
#Q1
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
    #Q2
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

