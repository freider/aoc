import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input



def part1():
    conv = sorted(int(line) for line in aoc_input().strip().split('\n'))
    last = conv[0]

    diffs = {}
    last = 0
    for c in conv:
        diff = c - last
        diffs[diff] = diffs.get(diff, 0) + 1
        last = c

    return diffs[1] * (diffs[3] + 1)



def part2():
    conv = sorted(int(line) for line in aoc_input().strip().split('\n'))

    mem = {}
    target = max(conv)

    def numways(c):
        if c == target:
            return 1
        if c in mem:
            return mem[c]

        ans = 0
        for p in conv:
            if p > c + 3:
                break
            if c < p:
                ans += numways(p)
        mem[c] = ans
        return ans

    return numways(0)


if __name__ == "__main__":
    print(part1())
    print(part2())
