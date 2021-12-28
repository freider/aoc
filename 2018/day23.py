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
    src = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""
    src = aoc_input()
    n = np.array([ints(l) for l in lines(src)])
    strong = np.argmax(n[:, 3])
    print(np.sum((np.sum(np.abs(n[:, :3] - n[strong, :3]), axis=1) <= n[strong, 3]) * 1))


def part2():
    """
    5432345
    4321234
    3210123
    4321234
    5432345


  2-2-2
  -1-1-
  2-0-2
  -1-1-
  2-2-2

    """

    # (x, y, r) => (top left corner), (bottom right corner) = (x - r, y), (x + r, y)
    #           # translate to rotated coords
    #           =>




if __name__ == "__main__":
    part1()
    part2()
