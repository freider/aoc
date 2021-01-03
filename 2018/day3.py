from collections import defaultdict, Counter

from lib.input import aoc_input, ints
from lib.point import Point

d = defaultdict(int)
paint = {}

for l in aoc_input().split('\n'):
    c, x, y, w, h = ints(l)
    for p in Point.range(Point(x, y), Point(x, y) + Point(w, h), inclusive=False):
        d[p] += 1
        paint[p] = c

print(sum(1 for x in d.values() if x >= 2))

for l in aoc_input().split('\n'):
    c, x, y, w, h = ints(l)

    if all(d[p] == 1 for p in Point.range(Point(x, y), Point(x, y) + Point(w, h), inclusive=False)):
        print(c)
        break
