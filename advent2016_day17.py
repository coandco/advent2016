import time
from collections import deque
from hashlib import md5
from typing import Deque, FrozenSet, Iterable, Tuple

from utils import BaseCoord as Coord
from utils import read_data

DIRS = {"U": Coord(x=0, y=-1), "R": Coord(x=1, y=0), "D": Coord(x=0, y=1), "L": Coord(x=-1, y=0)}
MAPPINGS = ["U", "D", "L", "R"]


def in_bounds(loc: Coord) -> bool:
    return 0 <= loc.x <= 3 and 0 <= loc.y <= 3


def doors_open(salt: str, path: str) -> FrozenSet[str]:
    hash_ = md5(f"{salt}{path}".encode()).hexdigest()[:4]
    return frozenset(MAPPINGS[i] for i in range(4) if hash_[i] in ("b", "c", "d", "e", "f"))


def all_paths(salt: str) -> Iterable[str]:
    startloc = Coord(0, 0)
    goal = Coord(3, 3)
    stack: Deque[Tuple[Coord, str]] = deque([(startloc, "")])
    while stack:
        loc, path = stack.popleft()
        if loc == goal:
            yield path
            continue
        possibilities = doors_open(salt, path)
        for heading in possibilities:
            new_loc = loc + DIRS[heading]
            if in_bounds(new_loc):
                stack.append((new_loc, path + heading))


def main():
    passcode = read_data()
    paths = list(all_paths(passcode))
    print(f"Part one: {min(paths, key=lambda x: len(x))}")
    print(f"Part two: {max(len(x) for x in paths)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
