import re
import time
from hashlib import md5
from typing import Dict, Iterable

from utils import read_data

TRIPLE = re.compile(r"(.)\1\1")
QUINTUPLE = re.compile(r"(.)\1\1\1\1")


def all_keys(salt: str, num_stretches: int = 0) -> Iterable[int]:
    i = 0
    three_indices: Dict[int, str] = {}
    valid_seen = set()
    while True:
        hash_ = md5(f"{salt}{i}".encode()).hexdigest()
        for _ in range(num_stretches):
            hash_ = md5(hash_.encode()).hexdigest()
        if match := TRIPLE.search(hash_):
            three_indices[i] = match.group(1)
        for five_match in QUINTUPLE.finditer(hash_):
            five_char = five_match.group(1)
            for j in range(max(0, i - 1000), i):
                if j not in valid_seen and three_indices.get(j) == five_char:
                    yield j
                    valid_seen.add(j)
        i += 1


def main():
    salt = read_data()
    keygen = all_keys(salt)
    print(f"Part one: {max(next(keygen) for _ in range(64))}")
    stretched_keygen = all_keys(salt, num_stretches=2016)
    print(f"Part two: {max(next(stretched_keygen) for _ in range(64))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
