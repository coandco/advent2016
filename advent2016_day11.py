import re
import time
from collections import deque
from functools import cache
from itertools import combinations
from typing import Deque, FrozenSet, Iterable, List, NamedTuple, Optional, Self, Tuple

from utils import read_data

GENERATORS_REGEX = re.compile(r"a ([a-z]+) generator")
CHIPS_REGEX = re.compile(r"a ([a-z]+)-compatible microchip")


class Floor(NamedTuple):
    items: FrozenSet[str]

    @classmethod
    def empty(cls):
        return Floor(frozenset())

    @property
    @cache
    def chips(self) -> FrozenSet[str]:
        return frozenset(x.lower() for x in self.items if x.isupper())

    @property
    @cache
    def generators(self) -> FrozenSet[str]:
        return frozenset(x for x in self.items if x.islower())

    @property
    @cache
    def unpaired_chips(self):
        return frozenset(x.upper() for x in self.chips - self.generators)

    @property
    @cache
    def unpaired_generators(self):
        return frozenset()

    def valid(self) -> bool:
        return (not self.generators) or (not self.unpaired_chips)

    def with_(self, arriving: Tuple[str, ...]) -> Self:
        return Floor(frozenset(self.items) | set(arriving))

    def without(self, leaving: Tuple[str, ...]) -> Self:
        return Floor(frozenset(self.items - set(leaving)))

    def valid_elevator_combinations(self) -> Iterable[Tuple[str, ...]]:
        for item in self.items:
            if self.without((item,)).valid():
                yield (item,)
        for combo in combinations(self.items, 2):
            if self.without(combo).valid():
                yield combo

    def __repr__(self):
        return f"[{','.join(self.items)}]"


class BuildingState(NamedTuple):
    elevator_floor: int
    floors: Tuple[Floor, ...]

    @classmethod
    def from_raw(cls, raw_data: str) -> Self:
        floors = []
        for i, line in enumerate(raw_data.splitlines()):
            generators: List[str] = [x[:2].lower() for x in GENERATORS_REGEX.findall(line)]
            chips: List[str] = [x[:2].upper() for x in CHIPS_REGEX.findall(line)]
            floors.append(Floor(frozenset(chips) | frozenset(generators)))
        return cls(elevator_floor=0, floors=tuple(floors))

    @property
    def anonymized(self):
        gens, chips = {}, {}
        for i, floor in enumerate(self.floors):
            for generator in floor.generators:
                gens[generator] = i
            for chip in floor.chips:
                chips[chip] = i
        # All pairs are interchangeable, so make a sorted list of pairs to remove the type from consideration
        raw_pairs = tuple(sorted((gens[x], chips[x]) for x in gens))
        return self.elevator_floor, raw_pairs

    def add_to_floor(self, floor_num: int, items: Tuple[str, ...]) -> Self:
        updated_floors = list(self.floors)
        updated_floors[floor_num] = self.floors[floor_num].with_(items)
        return BuildingState(self.elevator_floor, tuple(updated_floors))

    def valid(self):
        return all(x.valid() for x in self.floors)

    def move_up(self, items: Tuple[str, ...]) -> Optional[Self]:
        assert all(x in self.floors[self.elevator_floor].items for x in items), "Tried to move a nonexistent item!"
        if self.elevator_floor >= 3 or not self.floors[self.elevator_floor + 1].with_(items).valid():
            return None
        updated_floors = list(self.floors)
        updated_floors[self.elevator_floor] = self.floors[self.elevator_floor].without(items)
        updated_floors[self.elevator_floor + 1] = self.floors[self.elevator_floor + 1].with_(items)
        return BuildingState(elevator_floor=self.elevator_floor + 1, floors=tuple(updated_floors))

    def move_down(self, items: Tuple[str, ...]) -> Optional[Self]:
        assert all(x in self.floors[self.elevator_floor].items for x in items), "Tried to move a nonexistent item!"
        if self.elevator_floor <= 0 or not self.floors[self.elevator_floor - 1].with_(items).valid():
            return None
        updated_floors = list(self.floors)
        updated_floors[self.elevator_floor] = self.floors[self.elevator_floor].without(items)
        updated_floors[self.elevator_floor - 1] = self.floors[self.elevator_floor - 1].with_(items)
        return BuildingState(elevator_floor=self.elevator_floor - 1, floors=tuple(updated_floors))

    def victory_condition(self) -> Self:
        all_items = frozenset().union(*(x.items for x in self.floors))
        return BuildingState(elevator_floor=3, floors=(Floor.empty(), Floor.empty(), Floor.empty(), Floor(all_items)))


def shortest_victory(start_state: BuildingState) -> int:
    victory = start_state.victory_condition()
    seen = set()
    stack: Deque[Tuple[int, BuildingState]] = deque([(0, start_state)])
    while stack:
        steps, state = stack.popleft()
        if state == victory:
            return steps
        if state.anonymized in seen:
            continue
        seen.add(state.anonymized)
        for items in state.floors[state.elevator_floor].valid_elevator_combinations():
            if new_state := state.move_up(items):
                stack.append((steps + 1, new_state))
            if new_state := state.move_down(items):
                stack.append((steps + 1, new_state))
    raise Exception("Couldn't find a path to victory!")


def main():
    start_state = BuildingState.from_raw(read_data())
    print(f"Part one: {shortest_victory(start_state)}")
    hard_state = start_state.add_to_floor(0, ("el", "EL", "di", "DI"))
    print(f"Part two: {shortest_victory(hard_state)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
