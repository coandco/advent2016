from typing import List, Union
from utils import read_data

INPUT = read_data().split("\n")


def num_to_loc(grid: List[Union[None, int, str]], num: Union[int, str]):
    for index_y, row in enumerate(grid):
        for index_x, column in enumerate(row):
            if column == num:
                return [index_y, index_x]


def loc_to_num(grid: List[Union[None, int, str]], loc: List[int]):
    return grid[loc[0]][loc[1]]


def process_instruction(grid: List[Union[None, int, str]], loc: List[int], char: str):
    new_loc = list(loc)
    if char == 'U' and grid[loc[0] - 1][loc[1]] is not None:
        new_loc[0] -= 1
    elif char == 'D' and grid[loc[0] + 1][loc[1]] is not None:
        new_loc[0] += 1
    elif char == 'L' and grid[loc[0]][loc[1] - 1] is not None:
        new_loc[1] -= 1
    elif char == 'R' and grid[loc[0]][loc[1] + 1] is not None:
        new_loc[1] += 1
    return new_loc


def get_output(grid: List[Union[None, int, str]], data: List[str]):
    current_loc = num_to_loc(grid, 5)
    output = ""
    for line in data:
        for char in line:
            current_loc = process_instruction(grid, current_loc, char)
        output += str(loc_to_num(grid, current_loc))
    return output


PART_ONE_GRID = [[None, None, None, None, None],
                 [None, 1, 2, 3, None],
                 [None, 4, 5, 6, None],
                 [None, 7, 8, 9, None],
                 [None, None, None, None, None]]

PART_TWO_GRID = [[None, None, None, None, None, None, None],
                [None, None, None, 1,    None, None, None],
                [None, None, 2,    3,    4,    None, None],
                [None, 5,    6,    7,    8,    9,    None],
                [None, None, 'A',  'B',  'C',  None, None],
                [None, None, None, 'D',  None, None, None],
                [None, None, None, None, None, None, None]]

print(f"Part one solution: {get_output(PART_ONE_GRID, INPUT)}")
print(f"Part two solution: {get_output(PART_TWO_GRID, INPUT)}")
