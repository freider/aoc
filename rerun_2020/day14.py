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
    src = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    src = aoc_input()
    mem = {}
    zmask = omask = 0
    for l in lines(src):
        if l.startswith("mask"):
            mask = l.split(' = ')[-1]
            zmask = int(mask.replace('X', '1'), 2)
            omask = int(mask.replace('X', '0'), 2)
        else:
            _, loc, val = tokens(l)
            mem[loc] = (val & zmask) | omask

    print(sum(mem.values()))


def part2():
    src = aoc_input()
    mem = {}
    mask = ''
    npmask = np.array([])

    for l in lines(src):
        if l.startswith("mask"):
            mask = l.split(' = ')[-1]
            npmask = np.array([c for c in mask])
        else:
            _, loc, val = tokens(l)
            numx = mask.count('X')
            for i in range(2 ** numx):
                bini = bin(i)[2:]
                filler = np.array(['0']*(numx - len(bini)) + [c for c in bini])
                omask = npmask.copy()
                omask[npmask == 'X'] = filler
                zmask = omask.copy()
                zmask[npmask == '0'] = '1'
                mem[(loc & int(''.join(zmask), 2)) | int(''.join(omask), 2)] = val

    print(sum(mem.values()))


if __name__ == "__main__":
    part1()
    part2()
