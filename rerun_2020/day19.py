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
    src = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    src = aoc_input()
    rules, strings = chunks(src)

    r = {}

    for line in lines(rules):
        ri, rs = line.split(': ')
        # for p2, just swap out the rules
        if ri == '8':
            rs = '42 | 42 8'
        elif ri == '11':
            rs = '42 31 | 42 11 31'

        if '"' in rs:
            r[ri] = rs.strip('"')
        else:
            r[ri] = [s.split() for s in rs.split(' | ')]

    def matchrems(rule_i, s):
        rule = r[rule_i]
        if isinstance(rule, str):
            if s.startswith(rule):
                yield s[len(rule):]
        else:
            for seq in rule:
                last = [s]
                for sub_ri in seq:
                    newlast = []
                    for sub_s in last:
                        newlast += list(matchrems(sub_ri, sub_s))
                    last = newlast
                yield from iter(last)

    valid = 0
    for l in lines(strings):
        valid += any(len(rem) == 0 for rem in matchrems("0", l))
    print(valid)



def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
