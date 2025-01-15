import time
from collections import deque
from itertools import permutations

from utils import read_data


def scramble(raw_data: str, raw_instructions: str) -> str:
    data = deque(raw_data)
    for instruction in raw_instructions.splitlines():
        match instruction.split():
            case ["swap", "position", x, "with", "position", y]:
                x, y = int(x), int(y)
                data[x], data[y] = data[y], data[x]
            case ["swap", "letter", x, "with", "letter", y]:
                x, y = data.index(x), data.index(y)
                data[x], data[y] = data[y], data[x]
            case ["rotate", ("left" | "right") as direction, x, _]:
                direction = 1 if direction == "right" else -1
                data.rotate(direction * int(x))
            case ["rotate", "based", "on", "position", "of", "letter", x]:
                x = data.index(x)
                rotation_amount = 1 + x + (1 if x >= 4 else 0)
                data.rotate(rotation_amount)
            case ["reverse", "positions", x, "through", y]:
                x, y = int(x), int(y)
                tmplist = list(data)
                tmplist[x:y+1] = reversed(tmplist[x:y+1])
                data = deque(tmplist)
            case ["move", "position", x, "to", "position", y]:
                x, y = int(x), int(y)
                val = data[x]
                del data[x]
                data.insert(y, val)
    return "".join(data)

def unscramble(target: str, raw_instructions: str) -> str:
    for start_code in permutations("abcdefgh"):
        if scramble("".join(start_code), raw_instructions) == target:
            return "".join(start_code)


def main():
    print(f"Part one: {scramble("abcdefgh", read_data())}")
    print(f"Part two: {unscramble("fbgdceah", read_data())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
