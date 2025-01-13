import time
from collections import defaultdict, deque
from typing import Deque, Dict, Tuple

from utils import BaseCoord as Coord
from utils import read_data


def wall_at_x_y(pos: Coord, offset: int) -> bool:
    x, y = pos.x, pos.y
    if x < 0 or y < 0:
        return True
    value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + offset
    return value.bit_count() % 2 != 0


def min_to_dest(dest: Coord, offset: int) -> int:
    distances: Dict[Coord, int] = defaultdict(lambda: 999999)
    to_check: Deque[Tuple[int, Coord]] = deque([(0, Coord(1, 1))])
    while to_check:
        distance, loc = to_check.popleft()
        if distances[loc] <= distance:
            continue
        distances[loc] = distance
        if loc == dest:
            return distance
        for neighbor in loc.cardinal_neighbors():
            if not wall_at_x_y(neighbor, offset):
                to_check.append((distance + 1, neighbor))
    raise Exception("Failed to find a path to the destination")


def spider_to_fifty(offset: int) -> int:
    distances: Dict[Coord, int] = defaultdict(lambda: 999999)
    to_check: Deque[Tuple[int, Coord]] = deque([(0, Coord(1, 1))])
    while to_check:
        distance, loc = to_check.popleft()
        if distance > 50:
            continue
        if distances[loc] <= distance:
            continue
        distances[loc] = distance
        for neighbor in loc.cardinal_neighbors():
            if not wall_at_x_y(neighbor, offset):
                to_check.append((distance + 1, neighbor))
    return len(distances)


def main():
    offset = int(read_data())
    print(f"Part one: {min_to_dest(Coord(x=31, y=39), offset)}")
    print(f"Part two: {spider_to_fifty(offset)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
