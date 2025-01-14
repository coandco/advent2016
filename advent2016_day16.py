import time

from utils import read_data


def expand(data: str) -> str:
    return f'{data}0{"".join("1" if x == "0" else "0" for x in reversed(data))}'


def fill_disk(start_data: str, disk_size: int) -> str:
    curdata = start_data
    while len(curdata) < disk_size:
        curdata = expand(curdata)
    return curdata[:disk_size]


def checksum(data: str) -> str:
    while len(data) % 2 == 0:
        new_data = []
        for i in range(0, len(data), 2):
            first, second = data[i], data[i + 1]
            new_data.append("1" if first == second else "0")
        data = "".join(new_data)
    return data


def main():
    start_data = read_data()
    disk = fill_disk(start_data, 272)
    print(f"Part one: {checksum(disk)}")
    disk = fill_disk(start_data, 35651584)
    print(f"Part two: {checksum(disk)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
