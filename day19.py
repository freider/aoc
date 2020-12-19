from collections import defaultdict

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp
from lib.input import aoc_input, np_map, pb_input


def part1():
    rules, msg = aoc_input().strip().split('\n\n')
    d = {}
    for l in rules.split('\n'):
        i, mpart = l.split(": ")
        d[i] = [case.split() for case in mpart.split(" | ")]

    def matches(i, s):
        if '"' in i:
            m = i.strip('"')
            if s.startswith(m):
                yield len(m)
            else:
                return
        else:
            v = d[i]
            for case in v:
                ps = [0]
                for part in case:
                    new_ps = []
                    for p in ps:
                        for m in matches(part, s[p:]):
                            new_ps.append(p + m)
                    ps = new_ps
                yield from iter(ps)

    ans = 0
    for line in msg.split("\n"):
        ans += any(x == len(line) for x in matches('0', line))
    print(ans)


def part2():
    rules, msg = aoc_input().strip().split('\n\n')
    d = {}
    for l in rules.split('\n'):
        i, mpart = l.split(": ")
        if i == "8":
            mpart = "42 | 42 8"
        elif i == "11":
            mpart = "42 31 | 42 11 31"
        d[i] = [case.split() for case in mpart.split(" | ")]

    def matches(i, s):
        if '"' in i:
            m = i.strip('"')
            if s.startswith(m):
                yield len(m)
            else:
                return
        else:
            v = d[i]
            for case in v:
                ps = [0]
                for part in case:
                    new_ps = []
                    for p in ps:
                        for m in matches(part, s[p:]):
                            new_ps.append(p + m)
                    ps = new_ps
                yield from iter(ps)

    ans = 0
    for line in msg.split("\n"):
        ans += any(x == len(line) for x in matches('0', line))
    print(ans)

if __name__ == "__main__":
    part1()
    part2()
