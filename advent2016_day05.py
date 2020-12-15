import hashlib
from typing import List, Union, Tuple
from utils import read_data

INPUT = read_data()


def check_hash(door: str, index: int) -> Union[None, Tuple[int, int]]:
    text = "%s%s" % (door, index)
    hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    if hash.startswith("00000"):
        # print("Match found for text %s, hexdigest %s" % (text, hash))
        return hash[6], hash[5]
    else:
        return None


def update_password(passwd_list: List[str], character: str, position: int):
    try:
        position = int(position)
    except ValueError:
        # Hex digits don't always translate to ints.  Ignore ones that don't.
        return False

    if position < 0 or position > 7:
        # Out of bounds positions do nothing
        return False

    if passwd_list[position] == '_':
        passwd_list[position] = character

    if '_' not in passwd_list:
        return True
    else:
        return False


def part_one(data: str) -> str:
    output = ""
    index_int = 0
    for _ in range(8):
        current_char = None
        while current_char is None:
            current_char = check_hash(data, index_int)
            index_int += 1
        output += current_char[1]
    return output


def part_two(data: str) -> str:
    known_chars = ['_', '_', '_', '_', '_', '_', '_', '_']
    index_int = 0
    all_done = False

    while all_done is False:
        current_char = None
        while current_char is None:
            current_char = check_hash(data, index_int)
            index_int += 1
        all_done = update_password(known_chars, current_char[0], current_char[1])
        # print("Current password is %s" % "".join(known_chars))
    return "".join(known_chars)


print("Part one password is %s" % part_one(INPUT))
print("Part two password is %s" % part_two(INPUT))
