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
    src = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    src = aoc_input()
    blobs = chunks(src)
    rules = []
    for l in lines(blobs[0]):
        rules.append(ints(l, negative=False))

    err = 0
    rule_to_i = [set(range(len(rules))) for _ in range(len(rules))]
    for l in lines(blobs[2])[1:]:
        valid_tick = True
        ticknums = ints(l, negative=False)

        for n in ticknums:
            valid = False
            for r in rules:
                if r[0] <= n <= r[1] or r[2] <= n <= r[3]:
                    valid = True
            if not valid:
                valid_tick = False
                err += n

        if valid_tick:
            for i, n in enumerate(ticknums):
                for j, r in enumerate(rules):
                    if not (r[0] <= n <= r[1] or r[2] <= n <= r[3]):
                        rule_to_i[j].discard(i)
    print(err)
    sorted_rules = sorted(enumerate(rule_to_i), key=lambda i_s: len(i_s[1]))
    used = set()
    rule_i = {}
    for j, (i, allowed) in enumerate(sorted_rules):
        remaining =  allowed - used
        assert len(remaining) == 1
        r = remaining.pop()
        rule_i[i] = r
        used.add(r)

    print(rule_i)
    p2 = 1
    mytick = ints(blobs[1], negative=False)
    for i, l in enumerate(lines(blobs[0])):
        if l.startswith("departure"):
            p2 *= mytick[rule_i[i]]
    print(p2)

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
