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


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]

def addi(reg, a, b, c):
    reg[c] = reg[a] + b

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]

def muli(reg, a, b, c):
    reg[c] = reg[a] * b

def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]

def bani(reg, a, b, c):
    reg[c] = reg[a] & b

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]

def bori(reg, a, b, c):
    reg[c] = reg[a] | b

def setr(reg, a, b, c):
    reg[c] = reg[a]

def seti(reg, a, b, c):
    reg[c] = a

def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0

def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0

def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0

def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0

def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0

def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0



ops = {n: globals()[n] for n in "addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr".split()}

print(len(ops))


def part1():
    src = """"""
    src = aoc_input()
    testchunks = chunks(src.split('\n\n\n')[0])
    
    parsed = [[ints(l) for l in lines(tc)] for tc in testchunks]
    res = 0

    numfunk = {}

    for (pre, op, post) in parsed:
        poss = numfunk.setdefault(op[0], set())
        for opname, opfunk in ops.items():
            r = pre.copy()
            opfunk(r, *op[1:])
            if r == post:
                poss.add(opname)

        if len(poss) >= 3:
            res += 1
    
    used = set()
    sol = {}
    while len(used) < 16:
        rem = [(num, names - used) for num, names in numfunk.items() if names - used]
        opnr, opnames = min(rem, key=lambda x: len(x[1]))
        assert len(opnames) == 1
        opname = next(iter(opnames))
        sol[opnr] = opname
        used.add(opname)

    prg = [ints(l) for l in lines(src.split('\n\n\n')[1].strip())]
    reg = [0, 0, 0, 0]
    for instr in prg:
        print(instr)
        ops[sol[instr[0]]](reg, *instr[1:])
    print(reg[0])

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
