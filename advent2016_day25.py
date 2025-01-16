import time
from typing import Dict, List, Optional

from advent2016_day12 import ProgramState
from utils import read_data


def run_program(program: List[List[str]], modifications: Optional[Dict[str, int]] = None) -> List[int]:
    output = []
    if not modifications:
        modifications = {}
    current_state = ProgramState(**modifications)
    while 0 <= current_state.pc < len(program):
        op, *args = program[current_state.pc]
        if op == "out":
            output.append(current_state.resolve(args[0]))
            if len(output) == 8:
                return output
            current_state = ProgramState(**(current_state._asdict() | {"pc": current_state.pc + 1}))
        else:
            current_state = current_state.execute(op, args)


def main():
    program = [x.split() for x in read_data().splitlines()]
    a = 0
    while True:
        if run_program(program, {"a": a}) == ([0, 1] * 4):
            print(f"Part one: {a}")
            return
        a += 1


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
