import time
from collections import deque

from utils import read_data


def run_sim(num_elves: int) -> int:
    circle = deque(range(1, num_elves + 1))
    while len(circle) > 1:
        circle.rotate(-1)
        circle.popleft()
    return circle[0]


def run_sim_p2(num_elves: int) -> int:
    # Make two queues, since we're going to be ping-ponging back and forth across the circle
    left = deque(range(1, (num_elves // 2) + 1))
    right = deque(range((num_elves // 2) + 1, num_elves + 1))
    while left and right:
        # remove one from the bigger half
        left.pop() if len(left) > len(right) else right.popleft()
        # rotate
        right.append(left.popleft())
        left.append(right.popleft())
    return left[0] if left else right[0]


def main():
    print(f"Part one: {run_sim(int(read_data()))}")
    print(f"Part two: {run_sim_p2(int(read_data()))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
