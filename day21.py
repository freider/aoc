from copy import deepcopy

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
    lines = aoc_input().strip().split('\n')

    poss = {}
    entries = []
    all_i = set()
    for l in lines:
        ing, alg = l.split(" (")
        ing = ing.split(" ")
        all_i |= set(ing)
        alg = alg[9:].strip(")").split(", ")
        entries.append((ing, alg))
        for a in alg:
            if a not in poss:
                poss[a] = set(ing)
            else:
                poss[a] &= set(ing)

    risky = set.union(*poss.values())
    non_risky = all_i - risky
    s = 0
    for ing, alg in entries:
        s += len(non_risky & set(ing))
    print(s)
    return poss

def part2():
    poss = sorted(part1().items(), key=lambda x: len(x[1]))
    def do(i, used):
        if i == len(poss):
            return used
        ing, alg = poss[i]
        for a in alg:
            if a not in used:
                u = used.copy()
                u[a] = ing
                ans = do(i+1, u)
                if ans:
                    return ans

    ans = do(0, {})
    print(ans)
    print(",".join(y[0] for y in sorted(ans.items(), key=lambda x: x[1])))




if __name__ == "__main__":
    part1()
    part2()
