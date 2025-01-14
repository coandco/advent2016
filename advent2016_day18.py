import time
from typing import FrozenSet

from utils import read_data

TRAP_PATTERNS = {(True, True, False), (False, True, True), (False, False, True), (True, False, False)}


def next_traps(traps: FrozenSet[int], width: int) -> FrozenSet[int]:
    return frozenset(x for x in range(width) if (x - 1 in traps, x in traps, x + 1 in traps) in TRAP_PATTERNS)


def main():
    start, width = frozenset(i for i, x in enumerate(read_data()) if x == "^"), len(read_data())
    safe_tiles = 0
    cur_traps = start
    for i in range(400000):
        if i == 40:
            print(f"Part one: {safe_tiles}")
        safe_tiles += width - len(cur_traps)
        cur_traps = next_traps(cur_traps, width)
    print(f"Part two: {safe_tiles}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
