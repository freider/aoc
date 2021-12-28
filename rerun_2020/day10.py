import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    src = aoc_input()
    nums = ints(src)
    s = sorted(nums)
    o = defaultdict(int)
    for i in range(1, len(s)):
        o[s[i] - s[i-1]] += 1
    o[s[0]] += 1
    o[3] += 1
    print(o[1] * o[3])


def part2():
    src = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    src = aoc_input()
    nums = ints(src)
    s = sorted(nums)
    ways = [0] * (max(s) + 3)
    ways[0] = 1

    for ad in s:
        ways[ad] += ways[ad - 1] + ways[ad - 2] + ways[ad - 3]

    print(ways[max(s)])


if __name__ == "__main__":
    part1()
    part2()
