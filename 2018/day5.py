import re
from string import ascii_lowercase

from lib.input import aoc_input

f = aoc_input()

pats = []
for c in ascii_lowercase:
    C = c.upper()
    pats += [
        f"{c}{C}",
        f"{C}{c}"
    ]
p = re.compile("|".join(pats))


def red(f):
    while True:
        prev = len(f)
        f = p.sub("", f)
        if len(f) == prev:
            break
    return len(f)

print(red(f))

print(min(
red(f.replace(c, "").replace(c.upper(), ""))
for c in ascii_lowercase
))