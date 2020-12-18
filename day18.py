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


def next_expr2(toks):
    if toks[0] == "(":
        toks = toks[1:]
        cnt = 1
        for i, t in enumerate(toks):
            if t == "(":
                cnt += 1
            elif t == ")":
                cnt -= 1
            if cnt == 0:
                return ev2(toks[:i]), toks[i+1:]
    else:
        assert isinstance(toks[0], int)
        return toks[0], toks[1:]


def ev2(toks):
    tot, remaining = next_expr2(toks)
    stack = [tot]
    while remaining:
        op = remaining[0]
        remaining = remaining[1:]
        if op == "*":
            v, remaining = next_expr2(remaining)
            stack.append(v)
        elif op == "+":
            v, remaining = next_expr2(remaining)
            stack[-1] += v

    return reduce(lambda a, b: a * b, stack, 1)


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
    s = 0
    for line in lines:
        clean = line.replace(" ", "")
        toks = [int(c) if c.isdigit() else c for c in clean]
        s += ev2(toks)
    print(s)


if __name__ == "__main__":
    part1()
    part2()
