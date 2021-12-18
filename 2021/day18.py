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
    src = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
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
            return False, 0, n, 0

        a, b = n
        if outer_pars == 4:
            return True, a, 0, b

        done, addleft, mid, addright = expl(a, outer_pars + 1)
        if done:
            return True, addleft, [mid, addfirst(b, addright)], 0

        done, addleft, mid, addright = expl(b, outer_pars + 1)
        if done:
            return True, 0, [addlast(a, addleft), mid], addright

        return False, 0, [a, b], 0

    def join(n):
        if isinstance(n, int):
            if n >= 10:
                return True, [n // 2, (n + 1) // 2]
            else:
                return False, n
        ret = []
        did = False
        for sub in n:
            if not did:
                did, js = join(sub)
            else:
                js = sub
            ret.append(js)
        return did, ret

    def red(n):
        done = False
        while not done:
            done = True
            did, left, n, right = expl(n, 0)
            if did:
                done = False
                continue
            did, n = join(n)
            if did:
                done = False
                continue
        return n

    def mag(sf):
        if isinstance(sf, int):
            return sf
        return 3 * mag(sf[0]) + 2 * mag(sf[1])

    sm = reduce(lambda a, b: red([a, b]), nums)
    print(mag(sm))

    mx = 0
    for a in nums:
        for b in nums:
            if a != b:
                mx = max(mag(red([a, b])), mx)
    print(mx)


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
