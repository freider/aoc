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
from lib.numdict import numdict
from lib.point import Point


def part1():
    src = aoc_input()
    o, c2 = chunks(src)
    rules = dict(line.split(' -> ') for line in lines(c2))

    pol = o
    for i in range(10):
        nxt = [pol[0]]
        for j in range(1, len(pol)):
            pair = pol[j-1:j+1]
            if pair in rules:
                nxt += [rules[pair], pair[1]]
            else:
                nxt += [pair[1]]
        pol = ''.join(nxt)
    cnt = Counter(pol)
    mx = max(cnt.values()) - min(cnt.values())
    print(mx)


def part2():
    src = aoc_input()
    o, c2 = chunks(src)
    rules = dict(line.split(' -> ') for line in lines(c2))

    def expand(pair):
        a, c = pair
        b = rules[pair]
        return numdict({
            a + b: 1,
            b + c: 1
        })

    pol = numdict()
    for j in range(1, len(o)):
        pol = pol + {o[j-1:j+1]: 1}

    def rec(p, steps):
        if steps == 0:
            return p
        out = numdict()
        for pair, cnt in p.items():
            out = out + expand(pair) * cnt
        return rec(out, steps - 1)

    fin = rec(pol, 40)
    ret = {o[0]: 1}

    for (a, b), cnt in fin.items():
        ret[b] = ret.get(b, 0) + cnt

    mx = max(ret.values()) - min(ret.values())
    print(mx)


if __name__ == "__main__":
    part1()
    part2()
