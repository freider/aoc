import numbers
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
    src = aoc_input()
    nums = [eval(l) for l in lines(src)]

    def addfirst(q, p):
        if isinstance(q, int):
            return q + p
        return [addfirst(q[0], p), q[1]]

    def addlast(q, p):
        if isinstance(q, int):
            return q + p
        return [q[0], addlast(q[1], p)]

    def expl(n, outer_pars):
        if isinstance(n, int):
            return 0, n, 0

        a, b = n
        if outer_pars == 4:
            return a, 0, b

        addleft, mid, addright = expl(a, outer_pars + 1)
        if mid != a:
            return addleft, [mid, addfirst(b, addright)], 0

        addleft, mid, addright = expl(b, outer_pars + 1)
        if mid != b:
            return 0, [addlast(a, addleft), mid], addright

        return 0, [a, b], 0

    def join(n):
        if isinstance(n, int):
            if n >= 10:
                return [n // 2, (n + 1) // 2]
            else:
                return n
        ret = n.copy()
        for i in range(len(n)):
            ret[i] = join(n[i])
            if ret[i] != n[i]:
                return ret
        return ret

    def red(n):
        while 1:
            left, next_n, right = expl(n, 0)
            if next_n != n:
                n = next_n
                continue
            next_n = join(n)
            if next_n != n:
                n = next_n
                continue
            return n
        return n

    def mag(sf):
        if isinstance(sf, int):
            return sf
        return 3 * mag(sf[0]) + 2 * mag(sf[1])

    sm = reduce(lambda a, b: red([a, b]), nums)
    print(mag(sm))
    print(max(mag(red([a, b])) for a in nums for b in nums if a != b))


def part2():
    tok = pp.Literal('[') | pp.Word(pp.nums).set_parse_action(lambda x: int(x[0])) | pp.Literal(']') | pp.Literal(',').suppress()
    expr = pp.OneOrMore(tok)

    def expl(toks):
        c = 0
        for i, t in enumerate(toks):
            if t == '[':
                c += 1
            elif t == ']':
                c -= 1
            if c == 5:
                a, b = toks[i+1:i+3]
                p1 = toks[:i]
                p2 = toks[i+4:]
                for i in reversed(range(len(p1))):
                    if isinstance(p1[i], int):
                        p1[i] += a
                        break
                for i in range(len(p2)):
                    if isinstance(p2[i], int):
                        p2[i] += b
                        break

                return p1 + [0] + p2
        return toks

    def join(toks):
        for i in range(len(toks)):
            t = toks[i]
            if isinstance(t, int) and t >= 10:
                return toks[:i] + ['[', t // 2, (t + 1) // 2, ']'] + toks[i+1:]
        return toks

    def red(toks):
        while 1:
            t = expl(toks)
            if t != toks:
                toks = t
                continue
            t = join(toks)
            if t != toks:
                toks = t
                continue

            return toks

    def mag(toks):
        stack = []
        for t in toks:
            if t == ']':
                b, a = stack.pop(), stack.pop()
                stack.append(3 * a + 2 * b)
            elif isinstance(t, int):
                stack.append(t)
        return stack[0]

    src = aoc_input()

    def add(a, b):
        return red(['['] + a + b + [']'])

    parsed = [list(expr.parse_string(line)) for line in lines(src)]
    print(mag(reduce(add, parsed)))
    print(max(mag(add(p1, p2)) for p1 in parsed for p2 in parsed if p1 != p2))


if __name__ == "__main__":
    part1()
    part2()
