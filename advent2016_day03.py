from utils import read_data
from itertools import zip_longest
from typing import Iterable, List, Tuple

INPUT = read_data()

def grouper(iterable: Iterable, n: int, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def is_valid_triangle(num_list: List[int]) -> bool:
    biggest_num = max(num_list)
    return biggest_num < sum(num_list) - biggest_num


def part_one(data: List[str]) -> Tuple[int, int]:
    valid_triangle_count = 0
    invalid_triangle_count = 0
    for line in data:
        sides = [int(x) for x in line.strip().split()]
        if is_valid_triangle(sides):
            valid_triangle_count += 1
        else:
            invalid_triangle_count += 1
    return valid_triangle_count, invalid_triangle_count


def part_two(data: List[str]) -> Tuple[int, int]:
    valid_triangle_count = 0
    invalid_triangle_count = 0
    for group in grouper(data, 3):
        num_array = []
        for line in group:
            num_array.append([int(x) for x in line.strip().split()])
        for i in range(len(num_array)):
            sides = [x[i] for x in num_array]
            if is_valid_triangle(sides):
                valid_triangle_count += 1
            else:
                invalid_triangle_count += 1
    return valid_triangle_count, invalid_triangle_count


part_one_valid, _ = part_one(INPUT.split("\n"))
print("Number of valid triangles for part one: %s" % part_one_valid)
part_two_valid, _ = part_two(INPUT.split("\n"))
print("Number of valid triangles for part two: %s" % part_two_valid)
