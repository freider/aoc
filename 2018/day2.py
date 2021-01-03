from collections import Counter

from lib.input import aoc_input, tokens

twos = 0
threes = 0
for l in aoc_input().split('\n'):
    twos += 2 in Counter(l).values()
    threes += 3 in Counter(l).values()

print(twos * threes)

lines = tokens(aoc_input())

for a in lines:
    for b in lines:
        s = ''.join(c for c, d in zip(a, b) if c == d)
        if len(s) == len(a) - 1:
            print(s)
            exit()
