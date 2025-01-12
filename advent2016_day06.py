from collections import Counter
from typing import List
from utils import read_data

INPUT = read_data()


def make_counters(data: List[str]) -> List[Counter]:
    pos_counters = [Counter() for _ in range(8)]

    for line in data:
        for index, char in enumerate(line):
            pos_counters[index].update(char)
    return pos_counters


def part_one(counters: List[Counter]) -> str:
    return "".join([sorted(counters[i], key=lambda x: counters[i][x])[-1] for i in range(8)])


def part_two(counters: List[Counter]) -> str:
    return "".join([sorted(counters[i], key=lambda x: counters[i][x])[0] for i in range(8)])


processed_input = make_counters(INPUT.split("\n"))
print(f"Part one password: {part_one(processed_input)}")
print(f"Part two password: {part_two(processed_input)}")
