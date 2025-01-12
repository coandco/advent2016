import time
from typing import Dict, List, NamedTuple, Optional, Self

from utils import read_data

INSTRUCTIONS = {
    "cpy": lambda state, args: {args[1]: state.resolve(args[0]), "pc": state.pc + 1},
    "inc": lambda state, args: {args[0]: state.resolve(args[0]) + 1, "pc": state.pc + 1},
    "dec": lambda state, args: {args[0]: state.resolve(args[0]) - 1, "pc": state.pc + 1},
    "jnz": lambda state, args: {"pc": state.pc + int(args[1]) if state.resolve(args[0]) else state.pc + 1}
}


class ProgramState(NamedTuple):
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    pc: int = 0

    def resolve(self, ref: str):
        return getattr(self, ref) if ref.isalpha() else int(ref)

    def execute(self, op: str, args: List[str]) -> Self:
        return ProgramState(**(self._asdict() | INSTRUCTIONS[op](self, args)))


def run_program(program: List[List[str]], modifications: Optional[Dict[str, int]] = None) -> int:
    if not modifications:
        modifications = {}
    current_state = ProgramState(**modifications)
    while 0 <= current_state.pc < len(program):
        op, *args = program[current_state.pc]
        current_state = current_state.execute(op, args)
    return current_state.a


def main():
    program = [line.split() for line in read_data().splitlines()]
    print(f"Part one: {run_program(program)}")
    print(f"Part two: {run_program(program, modifications={"c": 1})}")



if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
