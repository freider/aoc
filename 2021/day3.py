import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens


def dec(s):
    r = 0
    for c in s:
        r *= 2
        r += c
    return r

def part1():
    lines = aoc_input().strip().split('\n')
    a = []
    b = []

    for i in range(len(lines[0])):
        z = sum(l[i] == "0" for l in lines)
        o = len(lines) - z

        if z > o:
            a.append(0)
            b.append(1)
        else:
            a.append(1)
            b.append(0)

    print(dec(a) * dec(b))


def part2():
    olines = aoc_input().strip().split('\n')
    lines = [l for l in olines]

    for i in range(len(lines[0])):
        if len(lines) == 1:
            break
        z = sum(l[i] == "0" for l in lines)
        o = len(lines) - z

        if z > o:
            lines = [l for l in lines if l[i] == "0"]
        else:
            lines = [l for l in lines if l[i] == "1"]

    a = [int(x) for x in lines[0]]

    lines = [l for l in olines]
    for i in range(len(lines[0])):
        if len(lines) == 1:
            break
        z = sum(l[i] == "0" for l in lines)
        o = len(lines) - z

        if z > o:
            lines = [l for l in lines if l[i] == "1"]
        else:
            lines = [l for l in lines if l[i] == "0"]

    b = [int(x) for x in lines[0]]
    print(dec(a) * dec(b))



if __name__ == "__main__":
    part1()
    part2()
