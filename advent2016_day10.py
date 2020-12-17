import re
from utils import read_data
from typing import NamedTuple, Tuple, List, Dict, Optional


class Bot(NamedTuple):
    id: int
    chips: Tuple[Optional[int], Optional[int]]

    @property
    def chip_list(self) -> List[Optional[int]]:
        return [x for x in self.chips if x is not None]

    @property
    def low_chip(self) -> int:
        assert len(self.chip_list) == 2, "Can't get low chip with zero or one chips"
        return min(self.chip_list)

    @property
    def high_chip(self) -> int:
        assert len(self.chip_list) == 2, "Can't get high chip with zero or one chips"
        return max(self.chip_list)

    @property
    def num_chips(self) -> int:
        return len(self.chip_list)

    def give_chips(self) -> Tuple[int, int, 'Bot']:
        chip_list = [x for x in self.chips if x is not None]
        assert len(chip_list) == 2, "Can't give high/low chips unless there are two"
        return self.low_chip, self.high_chip, Bot(self.id, (None, None))

    def receive_chip(self, chip: int) -> 'Bot':
        assert len(self.chip_list) < 2, "Can't receive a chip when all slots are already full"
        if len(self.chip_list) == 0:
            return Bot(id=self.id, chips=(chip, None))
        else:
            return Bot(id=self.id, chips=(self.chips[0], chip))

    def __repr__(self):
        return f"Bot(id={self.id}, chips={self.chips})"


class Transfer(NamedTuple):
    type: str
    id: int
    value: int

    @property
    def is_output(self) -> bool:
        return self.type == "output"


class Instruction(NamedTuple):
    from_id: int
    low_dest: str
    low_id: int
    high_dest: str
    high_id: int

    @property
    def low_is_output(self):
        return self.low_dest == "output"

    @property
    def high_is_output(self):
        return self.high_dest == "output"

    def is_active(self, bot_map: Dict[int, Bot]) -> bool:
        return len(bot_map[self.from_id].chip_list) == 2


NUMS_REGEX = re.compile(r"-?\d+")
INSTRUCTION_REGEX = re.compile(r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')


def process_input(data: List[str]) -> Tuple[Dict[int, Bot], List[Instruction]]:
    initial_values = [x for x in data if x.startswith("value")]
    instruction_list = [x for x in data if x.startswith("bot")]
    bot_map = {i: Bot(id=i, chips=(None, None)) for i in range(230)}
    for line in initial_values:
        value, bot_num = list(map(int, NUMS_REGEX.findall(line)))
        bot_map[bot_num] = bot_map[bot_num].receive_chip(value)
    parsed_instructions = []
    for line in instruction_list:
        line_match = INSTRUCTION_REGEX.match(line)
        bot_id, low_id, high_id = int(line_match.group(1)), int(line_match.group(3)), int(line_match.group(5))
        low_dest, high_dest = line_match.group(2), line_match.group(4)
        parsed_instructions.append(Instruction(bot_id, low_dest, low_id, high_dest, high_id))
    return bot_map, parsed_instructions


def run_instructions(bot_map: Dict[int, Bot], instruction_list: List[Instruction],
                     part_one_numbers: Tuple[int, int]) -> Dict[int, int]:
    outputs = {}
    while valid_instructions := [x for x in instruction_list if x.is_active(bot_map)]:
        for instruction in valid_instructions:
            low_value, high_value, bot_map[instruction.from_id] = bot_map[instruction.from_id].give_chips()
            if all(x in part_one_numbers for x in (low_value, high_value)):
                print(f"Part one: bot {instruction.from_id} is comparing {low_value} with {high_value}")

            if instruction.low_is_output:
                outputs[instruction.low_id] = low_value
            else:
                bot_map[instruction.low_id] = bot_map[instruction.low_id].receive_chip(low_value)

            if instruction.high_is_output:
                outputs[instruction.high_id] = high_value
            else:
                bot_map[instruction.high_id] = bot_map[instruction.high_id].receive_chip(high_value)

    return outputs


INPUT = read_data().split("\n")
bots, instructions = process_input(INPUT)
output = run_instructions(bots, instructions, (17, 61))
print(f"Part two: the product of output 0, 1, and 2 is {output[0]*output[1]*output[2]}")


