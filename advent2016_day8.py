import numpy
import re
from utils import read_data

INPUT = read_data()


def prettyprint_grid(grid: numpy.ndarray) -> int:
    total_lit = 0
    for row in grid:
        for item in row:
            if item == 0:
                print(" ", end='')
            elif item == 1:
                print("#", end='')
                total_lit += 1
        print("")  # No trailing end='', so it should yield a newline
    return total_lit


GRID = numpy.zeros((6, 50))

rect_regex = re.compile(r'^rect (\d+)x(\d+)')
row_regex = re.compile(r'rotate row y=(\d+) by (\d+)')
column_regex = re.compile(r'rotate column x=(\d+) by (\d+)')

for line in INPUT.split("\n"):
    match = rect_regex.match(line)
    if match is not None:
        GRID[:int(match.group(2)), :int(match.group(1))] = 1
        continue
    match = row_regex.match(line)
    if match is not None:
        GRID[int(match.group(1)), :] = numpy.roll(GRID[int(match.group(1)), :], int(match.group(2)))
        continue
    match = column_regex.match(line)
    if match is not None:
        GRID[:, int(match.group(1))] = numpy.roll(GRID[:, int(match.group(1))], int(match.group(2)))
        continue

num_lit = prettyprint_grid(GRID)
print("Total lit pixels: %d" % num_lit)
