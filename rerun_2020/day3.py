from collections import defaultdict

from lib.input import lines, aoc_input
from lib.point import Point

src = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
src = aoc_input()
m = lines(src)

w = len(m[0])
h = len(m)

s = defaultdict(int)

steps = [Point(1,1), Point(1,3), Point(1,5), Point(1,7), Point(2,1)]

for t in steps:
    c = Point(0, 0)
    while c[0] < h:
        if m[c[0]][c[1] % w] == "#":
            s[t] += 1
        c += t

print(s)
import numpy as np
print(np.product(np.array(list(s.values()))))
