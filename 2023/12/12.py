import numpy as np
from functools import lru_cache
from tqdm import tqdm

input_data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split("\n")

with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]


@lru_cache(maxsize=None)
def num_possible_arrangements(spring_map: tuple[int], spring_list: tuple[int]):
    spring_map = np.array(spring_map)
    spring_list = np.array(spring_list)
    first_value = spring_list[0]
    max_first_value_pos = (
        len(spring_map) - spring_list[1:].sum() - len(spring_list) - first_value + 1
    )
    result = 0
    for i in range(max_first_value_pos + 1):
        if spring_map[i : i + first_value].prod() == 0:
            continue
        if (spring_map[:i] == 1).sum() > 0:
            continue
        if i + first_value < len(spring_map) and spring_map[i + first_value] == 1:
            continue
        if len(spring_list) == 1:
            if (spring_map[i + first_value + 1 :] == 1).sum() == 0:
                result += 1
        else:
            result += num_possible_arrangements(
                tuple(spring_map[i + first_value + 1 :].tolist()),
                tuple(spring_list[1:].tolist()),
            )
    return result


mapping_dict = {".": 0, "#": 1, "?": -1}
result_q1 = 0
result_q2 = 0
for i, line in enumerate(tqdm(input_data)):
    data1, data2 = line.split(" ")
    springs = np.array(list(map(int, data2.split(","))))
    springs_map = np.array([mapping_dict[c] for c in data1])
    result_q1 += num_possible_arrangements(
        tuple(springs_map.tolist()), tuple(springs.tolist())
    )
    springs = np.array(list(map(int, ",".join([data2] * 5).split(","))))
    springs_map = np.array([mapping_dict[c] for c in "?".join([data1] * 5)])
    result_q2 += num_possible_arrangements(
        tuple(springs_map.tolist()), tuple(springs.tolist())
    )


print(result_q1)
print(result_q2)
