import time
from collections import defaultdict, deque
from itertools import permutations
from typing import Deque, Dict, Set, Tuple

from utils import BaseCoord as Coord
from utils import read_data, read_grid


class Ducts:
    walls: Set[Coord]
    points: Dict[int, Coord]
    distances: Dict[int, Dict[int, int]]

    def __init__(self, raw_maze: str):
        self.walls = set()
        self.points = {}
        for loc, char in read_grid(raw_maze):
            if char == "#":
                self.walls.add(loc)
            elif char.isnumeric():
                self.points[int(char)] = loc
        self.distances = {}
        for num, point in self.points.items():
            distances = self.distances_from_loc(point)
            self.distances[num] = {k: distances[v] for k, v in self.points.items() if k != num}

    def distances_from_loc(self, startloc: Coord) -> Dict[Coord, int]:
        distances = defaultdict(lambda: 99999)
        stack: Deque[Tuple[int, Coord]] = deque([(0, startloc)])
        while stack:
            distance, loc = stack.popleft()
            if distances[loc] <= distance:
                continue
            distances[loc] = distance
            for neighbor in loc.cardinal_neighbors():
                if neighbor not in self.walls:
                    stack.append((distance + 1, neighbor))
        return distances

    def distance_for_pattern(self, pattern: Tuple[int, ...]) -> int:
        return sum(self.distances[pattern[i]][pattern[i + 1]] for i in range(len(pattern) - 1))

    def shortest_distance(self) -> int:
        non_start_points = (x for x in self.distances.keys() if x != 0)
        return min(self.distance_for_pattern((0,) + x) for x in permutations(non_start_points))

    def shortest_distance_with_return(self) -> int:
        non_start_points = (x for x in self.distances.keys() if x != 0)
        return min(self.distance_for_pattern((0,) + x + (0,)) for x in permutations(non_start_points))


def main():
    ducts = Ducts(read_data())
    print(f"Part one: {ducts.shortest_distance()}")
    print(f"Part one: {ducts.shortest_distance_with_return()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
