from collections import defaultdict
from math import factorial
from typing import List, Optional, Dict

from advent2016_day12 import ProgramState

from utils import read_data
import time

def run_program(program: List[List[str]], modifications: Optional[Dict[str, int]] = None) -> int:
    if not modifications:
        modifications = {}
    current_state = ProgramState(**modifications)
    line_counts = defaultdict(int)
    while 0 <= current_state.pc < len(program):
        line_counts[current_state.pc] += 1
        op, *args = program[current_state.pc]
        if op == "tgl":
            addr = current_state.pc + current_state.resolve(args[0])
            if 0 <= addr < len(program):
                print(f"Toggling instruction {addr} ({program[addr]})")
                if len(program[addr]) == 3:
                    program[addr][0] = "cpy" if program[addr][0] == "jnz" else "jnz"
                else:
                    program[addr][0] = "dec" if program[addr][0] == "inc" else "inc"
            current_state = ProgramState(**(current_state._asdict() | {"pc": current_state.pc + 1}))
        else:
            try:
                current_state = current_state.execute(op, args)
            except Exception as e:
                print(f"Hit bad instruction {op} {args}: {e}")
                current_state = ProgramState(**(current_state._asdict() | {"pc": current_state.pc + 1}))
    return current_state.a

# Everything above this line is for historical purposes only
def translated(program: List[List[str]], num_eggs: int) -> int:
    constant = int(program[19][1]) * int(program[20][1])
    return factorial(num_eggs) + constant


def main():
    program = [line.split() for line in read_data().splitlines()]
    print(f"Part one: {translated(program, 7)}")
    print(f"Part two: {translated(program, 12)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
