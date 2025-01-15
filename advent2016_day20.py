import time
from typing import List

from utils import read_data


def pop_merged_bottom(sorted_blocks: List[range]) -> range:
    bottom_range = sorted_blocks.pop()
    while sorted_blocks:
        new_range = sorted_blocks.pop()
        # If the ranges overlap or abut, merge them into the bottom range
        if range(max(bottom_range.start, new_range.start - 1), min(bottom_range.stop, new_range.stop)):
            bottom_range = range(bottom_range.start, max(bottom_range.stop, new_range.stop))
            continue
        # The one we just looked at isn't part of the set, so put it back on the list
        sorted_blocks.append(new_range)
        break
    # This mutates sorted_blocks when it runs to remove ranges that have been merged
    return bottom_range


def main():
    unsorted_blocks = [range(int(x.split("-")[0]), int(x.split("-")[1]) + 1) for x in read_data().splitlines()]
    # Sort it with the lowest-starting ranges at the end, for efficient popping/pushing
    blocks = sorted(unsorted_blocks, key=lambda x: x.start, reverse=True)
    bottom_range = pop_merged_bottom(blocks)
    print(f"Part one: {bottom_range.stop}")
    num_allowed = 0
    while blocks:
        old_end = bottom_range.stop
        bottom_range = pop_merged_bottom(blocks)
        num_allowed += len(range(old_end, bottom_range.start))
    num_allowed += len(range(bottom_range.stop, 4294967295 + 1))
    print(f"Part two: {num_allowed}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
