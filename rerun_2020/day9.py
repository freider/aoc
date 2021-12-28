import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints
from lib.point import Point


def part1():
    src = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    le = 5
    src = aoc_input()
    le = 25
    nums = ints(src)
    for i in range(le, len(nums)):
        prev = nums[i - le:i]

        good = False
        for j in range(le):
            for k in range(le):
                if j != k:
                    if prev[k] + prev[j] == nums[i]:
                        good = True
                        break
            if good:
                break

        if not good:
            print(nums[i])
            break


def part2():
    src = aoc_input()
    arr = np.array(ints(src))
    cs = np.cumsum(arr)
    for i in range(len(cs)):
        for j in range(i+2, len(cs)):
            if cs[j] - cs[i] == 776203571:
                print(min(arr[i:j]) + max(arr[i:j]))
                return




if __name__ == "__main__":
    part1()
    part2()
