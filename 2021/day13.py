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
    points = []
    for l in lines(cs[0]):
        points.append(tuple(ints(l)[::-1]))

    shape = np.max(np.array(points), axis=0) + 1
    m = np.zeros(shape, dtype=int)

    for p in points:
        m[p] = 1

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
    pass


if __name__ == "__main__":
    part1()
    part2()



pic = """
###   ##  #  # #### ###  ####   ##  ## 
#  # #  # #  #    # #  # #       # #  #
#  # #    ####   #  ###  ###     # #   
###  # ## #  #  #   #  # #       # #   
#    #  # #  # #    #  # #    #  # #  #
#     ### #  # #### ###  #     ##   ## 
"""

msg, rem = decode_string(pic)
print(msg)
draw(rem, charmap={0: ' ', 1: '#'})
