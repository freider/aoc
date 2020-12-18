import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def next_expr(toks):
    if toks[0] == "(":
        toks = toks[1:]
        cnt = 1
        for i, t in enumerate(toks):
            if t == "(":
                cnt += 1
            elif t == ")":
                cnt -= 1
            if cnt == 0:
                # print("grp", toks, toks[:i], t)
                return ev(toks[:i]), toks[i+1:]
    else:
        assert isinstance(toks[0], int)
        return toks[0], toks[1:]

def ev(toks):
    tot, remaining = next_expr(toks)
    while remaining:
        op = remaining[0]
        remaining = remaining[1:]
        assert op not in ")("
        if op == "*":
            v, remaining = next_expr(remaining)
            tot *= v
        elif op == "+":
            v, remaining = next_expr(remaining)
            tot += v

    return tot

def part1():
    lines = aoc_input().strip().split('\n')
    s = 0
    for line in lines:
        clean = line.replace(" ", "")
        toks = [int(c) if c.isdigit() else c for c in clean]
        s += ev(toks)
    print(s)




def part2():
    lines = aoc_input().strip().split('\n')



if __name__ == "__main__":
    part1()
    part2()
