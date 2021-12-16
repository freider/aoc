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


allvers = []

def literal(bits):
    numbits = []
    i = 0
    while True:
        numbits.append(bits[i+1:i+5])
        if bits[i] == "0":
            i += 5
            break
        i += 5
    return bits[i:], ''.join(numbits)


def operator(op, bits):
    lti = bits[0]
    if lti == "0":
        bitlen = int(bits[1: 1 + 15], 2)
        subpacks = []
        packres = bits[16:16 + bitlen]
        while packres:
            packres, res = packet(packres)
            subpacks.append(res)

        rem = bits[16 + bitlen:]
    else:
        numsubs = int(bits[1: 1 + 11], 2)
        subpacks = []
        rem = bits[12:]
        for i in range(numsubs):
            rem, res = packet(rem)
            subpacks.append(res)

    if op == 0:
        return rem, sum(subpacks)
    if op == 1:
        return rem, np.product(subpacks)
    if op == 2:
        return rem, min(subpacks)
    if op == 3:
        return rem, max(subpacks)
    if op == 5:
        return rem, 1 if subpacks[0] > subpacks[1] else 0
    if op == 6:
        return rem, 1 if subpacks[0] < subpacks[1] else 0
    if op == 7:
        return rem, 1 if subpacks[0] == subpacks[1] else 0

    return rem, subpacks


def packet(bits):
    version = bits[:3]
    allvers.append(int(version, 2))
    typeid = bits[3:6]
    if int(typeid, 2) == 4:
        rem, lit = literal(bits[6:])
        return rem, int(lit, 2)
    else:
        rem, res = operator(int(typeid, 2), bits[6:])
        return rem, res

def part1():
    src = """EE00D40C823060"""
    src = aoc_input().strip()
    bitsa = []
    for c in src:
        rawbin = bin(int(c, 16))[2:]
        padded = (4 - len(rawbin)) * "0" + rawbin
        bitsa.append(padded)
    bits = ''.join(bitsa)

    print(packet(bits))
    print(sum(allvers))





def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
