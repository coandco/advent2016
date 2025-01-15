from collections import deque, defaultdict
from itertools import permutations
from typing import NamedTuple, Dict, Deque, Tuple

from utils import read_data, BaseCoord as Coord
import time
import re

DIGITS = re.compile(r"\d+")


class Node(NamedTuple):
    total: int
    used: int

    @property
    def free(self):
        return self.total - self.used


def load_nodes(raw_data: str) -> Dict[Coord, Node]:
    nodes: Dict[Coord, Node] = {}
    for line in raw_data.splitlines()[2:]:
        x, y, total, used, free, percent = (int(x) for x in DIGITS.findall(line))
        assert free == total - used
        nodes[Coord(x=x, y=y)] = Node(total, used)
    return nodes


def get_distances(nodes: Dict[Coord, Node]) -> Dict[Coord, int]:
    walls = {k for k, v in nodes.items() if v.used > 100}
    start_loc = next(k for k, v in nodes.items() if v.used == 0)
    max_x, max_y = max(n.x for n in nodes), max(n.y for n in nodes)
    distances: Dict[Coord, int] = defaultdict(lambda: 99999)
    stack: Deque[Tuple[int, Coord]] = deque([(0, start_loc)])
    while stack:
        distance, loc = stack.popleft()
        if distances[loc] <= distance:
            continue
        distances[loc] = distance
        for neighbor in loc.cardinal_neighbors():
            if 0 <= loc.x <= max_x and 0 <= loc.y <= max_y and loc not in walls:
                stack.append((distance + 1, neighbor))
    return distances


def min_moves(nodes: Dict[Coord, Node]) -> int:
    walls = {k for k, v in nodes.items() if v.used > 100}
    assert all(n.y > 2 for n in walls), "This algorithm doesn't work if large nodes are too high"
    max_x = max(n.x for n in nodes)
    # Use A* to figure out how much it costs to get to the goal node,
    # at which point the goal will be moved one to the left
    initial_move_cost = get_distances(nodes)[Coord(x=max_x, y=0)]
    # Each horizontal move costs 5 (down/left/left/left/up/right)
    horizontal_move_cost = 5 * (max_x - 1)
    return initial_move_cost + horizontal_move_cost


def main():
    nodes = load_nodes(read_data())
    print(f"Part one: {sum(1 for x, y in permutations(nodes.values(), 2) if 0 < x.used < y.free)}")
    print(f"Part two: {min_moves(nodes)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
