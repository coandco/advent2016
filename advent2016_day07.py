import regex as re
from utils import read_data
from typing import Tuple, List, List

def contains_abba(string: str) -> bool:
    matcher = re.compile(r'(.)(?!\1)(.)\2\1')
    return matcher.search(string) is not None


def parse_address(string: str) -> Tuple[List[str], List[str]]:
    parsed = [x.split(']') for x in string.split('[')]
    outsides = []
    insides = []
    for group in parsed:
        if len(group) == 1:
            outsides.append(group[0])
        elif len(group) == 2:
            insides.append(group[0])
            outsides.append(group[1])
    return outsides, insides


def supports_tls(outsides: List[str], insides: List[str]) -> bool:
    for inside in insides:
        if contains_abba(inside):
            return False
    for outside in outsides:
        if contains_abba(outside):
            return True
    return False


def supports_ssl(outsides: List[str], insides: List[str]) -> bool:
    possible_matches = []
    matcher = re.compile(r'(.)(?!\1)(.)\1')
    for outside in outsides:
        for thing in matcher.finditer(outside, overlapped=True):
            possible_matches.append((thing.group(0), "%s%s%s" % (thing.group(2), thing.group(1), thing.group(2))))
    if len(possible_matches) == 0:
        return False
    matcher = re.compile("|".join([x[1] for x in possible_matches]))
    for inside in insides:
        if matcher.search(inside) is not None:
            #print("SSL match found for %r, %r, %r" % (outsides, insides, possible_matches))
            return True
    #print("No SSL match found for %r, %r, %r" % (outsides, insides, possible_matches))
    return False


num_tls = 0
num_ssl = 0
for line in read_data().split("\n"):
    outsides, insides = parse_address(line)
    if supports_tls(outsides, insides):
        num_tls += 1
    if supports_ssl(outsides, insides):
        num_ssl += 1

print("Total TLS: %d" % num_tls)
print("Total SSL: %d" % num_ssl)
