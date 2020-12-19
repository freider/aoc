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


import pyparsing as pp


def part1_pp():
    def calc(terms):
        val = terms[0]
        for i in range(1, len(terms), 2):
            op = terms[i]
            if op == "+":
                val += terms[i+1]
            else:
                val *= terms[i+1]
        return val

    o = pp.infixNotation(pp.pyparsing_common.integer, [
        (pp.oneOf("+ *"), 2, pp.opAssoc.LEFT, lambda toks: calc(toks[0])),
    ])
    print(sum(o.parseString(l)[0] for l in aoc_input().strip().split('\n')))


def part2_pp():
    mult = lambda l: reduce(lambda a, b: a * b, l, 1)  # multiply a list
    o = pp.infixNotation(pp.pyparsing_common.integer, [
        (pp.Suppress("+"), 2, pp.opAssoc.LEFT, lambda tok: sum(tok[0])),
        (pp.Suppress("*"), 2, pp.opAssoc.LEFT, lambda tok: mult(tok[0]))
    ])
    print(sum(o.parseString(l)[0] for l in aoc_input().strip().split('\n')))


if __name__ == "__main__":
    # part1()
    # part1_pp()
    # part2()
    # part2_pp()

    o = pp.infixNotation(pp.pyparsing_common.integer, [
        (pp.oneOf("+ *"), 2, pp.opAssoc.LEFT),
    ])
    o.parseString("5 + 2 * 3 + 1 + 2").pprint()
