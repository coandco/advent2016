from utils import read_data
from typing import Generator


def tokenize_data(data: str, recurse: bool = False) -> Generator[int, None, None]:
    current_loc = 0
    while current_loc < len(data):
        if data[current_loc] == "(":
            start, end = current_loc + 1, current_loc + data[current_loc:].index(")")
            raw_length, times = (int(x) for x in data[start:end].split("x"))
            full_length = raw_length
            if recurse and "(" in data[end+1:end+1+raw_length]:
                full_length = sum(tokenize_data(data[end+1:end+1+raw_length], recurse=recurse))
            yield full_length * times
            current_loc = (end + raw_length + 1)
        else:
            yield 1
            current_loc += 1


INPUT = read_data()
print(f"Part one: {sum(tokenize_data(INPUT))}")
print(f"Part two: {sum(tokenize_data(INPUT, recurse=True))}")
