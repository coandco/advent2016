import re
import string
from collections import Counter
from utils import read_data

INPUT = read_data()


def common_letters(text):
    frequencies = Counter(text)
    del frequencies['-']
    return sorted(sorted(frequencies), key=lambda x: frequencies[x], reverse=True)[:5]


def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)


matcher = re.compile(r'^([a-z-]*)-([0-9]+)\[([a-z]{5})\]$')

total = 0
object_storage_sector = None
for line in INPUT.split("\n"):
    match = matcher.match(line)
    code = "".join(common_letters(match.group(1)))
    if code == match.group(3):
        # print("Checksum %s for %s is good with sector id %s" % (code, match.group(1), match.group(2)))
        decrypted_text = caesar(match.group(1), int(match.group(2)) % 26)
        print("Decrypted text for sector %s is %s" % (match.group(2), decrypted_text))
        total += int(match.group(2))
        if decrypted_text == "northpole-object-storage":
            object_storage_sector = match.group(2)
    else:
        pass
        # print("Checksum %s for %s is bad" % (code, match.group(1)))

print("Total is: %d" % total)
print("Object storage sector: %s" % object_storage_sector)