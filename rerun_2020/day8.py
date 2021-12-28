import sys
import re
from collections import Counter, defaultdict
from copy import deepcopy

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints, lines
from lib.point import Point


def part1():
    src = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    src = aoc_input()
    acc = 0
    prg = []
    for l in lines(src):
        prg.append(tokens(l, negative=True))
    i = 0

    done = set()
    while i not in done:
        instr, n = prg[i]
        done.add(i)
        if instr == "nop":
            i += 1
            continue
        if instr == "acc":
            acc += n
            i += 1
            continue
        if instr == "jmp":
            i += n

    print(acc)


def part2():
    src = aoc_input()

    prg = []
    for l in lines(src):
        prg.append(list(tokens(l, negative=True)))

    def exec(p):
        acc = 0
        i = 0

        done = set()
        while i not in done:
            if i == len(p):
                return acc
            instr, n = p[i]
            done.add(i)
            if instr == "nop":
                i += 1
                continue
            if instr == "acc":
                acc += n
                i += 1
                continue
            if instr == "jmp":
                i += n
        return None

    for i in range(len(prg)):
        p = deepcopy(prg)
        if prg[i][0] == "nop":
            p[i][0] = "jmp"
        elif prg[i][0] == "jmp":
            p[i][0] = "nop"
        else:
            continue

        v = exec(p)
        if v is not None:
            print(v)
            return



if __name__ == "__main__":
    part1()
    part2()
