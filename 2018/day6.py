from collections import defaultdict

from lib.input import aoc_input, ints
import numpy as np

from lib.point import Point

coords = np.array([ints(l) for l in aoc_input().split("\n")])

minx, miny = coords.min(axis=0)
maxx, maxy = coords.max(axis=0)


def close(p):
    dists = np.abs(coords - p.np()).sum(axis=1)
    minval = dists.min()
    ix, = np.where(dists == minval)
    if len(ix) > 1:
        return None
    return ix[0]


s = defaultdict(int)
for p in Point.range(Point(minx, miny), Point(maxx, maxy)):
    s[close(p)] += 1

for x in range(minx, maxx+1):
    s.pop(close(Point(x, miny)), None)
    s.pop(close(Point(x, maxy)), None)

for y in range(miny, maxy+1):
    s.pop(close(Point(minx, y)), None)
    s.pop(close(Point(maxx, y)), None)

print(max(s.values()))


a = 0
for p in Point.range(Point(minx - 200, miny - 200), Point(maxx + 200, maxy + 200)):
    a += int(np.abs(coords - p.np()).sum() < 10000)

print(a)