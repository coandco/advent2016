from utils import read_data
from typing import NamedTuple, Tuple, Union, TypeVar


class Floor(NamedTuple):
    chips: Tuple[str, ...]
    generators: Tuple[str, ...]

    def validate(self):
        all(x in self.generators for x in self.chips)

    def valid_elevator_combinations(self):
        


class BuildingState(NamedTuple):
    elevator_floor: int
    floors: Tuple[Floor, Floor, Floor, Floor]

    def validate(self):
        return all(x.validate() for x in self.floors)
