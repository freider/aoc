import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp
from sympy import simplify, Symbol
from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = aoc_input()
    chunks = src.split('inp w\n')

    chunknums = []
    for c in chunks[1:]:
        a, b, d = None, None, None
        for l in lines(c):
            nums = ints(l)
            if l.startswith('div'):
                assert d is None
                d = nums[0]
            elif l.startswith('add x') and len(nums) > 0:
                assert a is None
                a = nums[0]
            elif l.startswith('add y') and len(nums) > 0:
                b = nums[0]
        chunknums.append((a, b, d))

    print("constants", [d for _, _, d in chunknums])
    
    # w = inp
    # x = (z % 26 + a) != w
    # z = z // d + x(25(z//d) + w + b)

    cnt = [0]
    def rec(groupi, usedw, lastz):
        if groupi == 3:
            print(cnt[0], '/', 10000)
            cnt[0] += 1

        remdiv = np.prod([x for _, _, x in chunknums[groupi + 1:]])

        if groupi == len(chunknums):
            if lastz == 0:
                return usedw
            else:
                print('So close', lastz)

        a, b, d = chunknums[groupi]
        for w in range(1, 10):  # <-- this is for part2. Add reversed() around the range to get part1 solution
            xval = lastz % 26 + a != w
            tz = lastz // d
            newz = tz + xval * (25 * tz + w + b)
            if newz < remdiv:
                res = rec(groupi + 1, usedw + [w], newz)
                if res:
                    return res

    print(''.join(str(x) for x in rec(0, [], 0)))



def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
