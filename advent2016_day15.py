import re
import time
from typing import Iterable, List, NamedTuple

from utils import read_data

DIGITS = re.compile(r"\d+")


class Disc(NamedTuple):
    position: int
    mod: int
    offset: int

    @staticmethod
    def from_line(line: str) -> "Disc":
        position, mod, _, offset = (int(x) for x in DIGITS.findall(line))
        return Disc(position, mod, offset)

    def is_time_good(self, time_: int) -> bool:
        return (time_ + self.position + self.offset) % self.mod == 0

    def good_times(self) -> Iterable[int]:
        curtime = 0
        for i in range(self.mod):
            if self.is_time_good(i):
                curtime = i
                yield i
        while True:
            curtime += self.mod
            yield curtime


def find_good_time(discs: List[Disc]) -> int:
    biggest_mod = max(discs, key=lambda x: x.mod)
    for t in biggest_mod.good_times():
        if all(x.is_time_good(t) for x in discs):
            return t


def main():
    discs = [Disc.from_line(x) for x in read_data().splitlines()]
    print(f"Part one: {find_good_time(discs)}")
    discs.append(Disc(discs[-1].position + 1, 11, 0))
    print(f"Part two: {find_good_time(discs)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
