import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks


def part1():
    lines = aoc_input().strip()


    chs = chunks(lines)
    nums = tokens(chs[0])

    boards = []
    for c in chs[1:]:
        boards.append([tokens(l) for l in c.split('\n')])

    def wins(b, ns):
        alnums = set(ns)

        for i in range(5):
            row = set(b[i])
            col = set(b[j][i] for j in range(5))
            if not (row - alnums) or not (col - alnums):
                return True

    def score(b, ns):
        alnums = set(ns)
        s = 0
        for i in range(5):
            s += sum(set(b[i]) - set(alnums))
        return s * ns[-1]

    for i in range(len(nums)):
        for b in boards:
            if wins(b, nums[:i+1]):
                print(score(b, nums[:i+1]))
                return


def part2():
    lines = aoc_input().strip()


    chs = chunks(lines)
    nums = tokens(chs[0])

    boards = []
    for c in chs[1:]:
        boards.append([tokens(l) for l in c.split('\n')])

    def wins(b, ns):
        alnums = set(ns)

        for i in range(5):
            row = set(b[i])
            col = set(b[j][i] for j in range(5))
            if not (row - alnums) or not (col - alnums):
                return True

    def score(b, ns):
        alnums = set(ns)
        s = 0
        for i in range(5):
            s += sum(set(b[i]) - set(alnums))
        return s * ns[-1]

    for i in range(len(nums)):
        for b in boards:
            if wins(b, nums[:i+1]):
                if len(boards) == 1:
                    print(score(b, nums[:i+1]))
                    return
                else:
                    boards = [c for c in boards if c != b]


if __name__ == "__main__":
    part1()
    part2()
