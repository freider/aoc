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
from lib.ocr import decode_array, decode_string
from lib.point import Point


def part1():
    src = aoc_input()
    cs = chunks(src)
    m = sparse_to_array({tuple(ints(l))[::-1]: 1 for l in lines(cs[0])})

    for i, instr in enumerate(lines(cs[1])):
        val, = ints(instr)
        if 'y' in instr:
            assert val == m.shape[0] // 2
            m = m[:val, :] | m[(val + 1):, :][::-1, :]
        else:
            assert val == m.shape[1] // 2
            m = m[:, :val] | m[:, (val + 1):][:, ::-1]

        if i == 0:
            print(m.sum())

    msg, unmatched = decode_array(m)
    print(msg)


def part2():
    cs = chunks(aoc_input())
    print()



if __name__ == "__main__":
    part1()
    part2()
