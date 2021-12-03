import re
import sys
from functools import reduce
from operator import mul

import networkx as nx
import numpy as np
import pyparsing as pp

from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input, tokens


def part1():
    x, y = 0, 0
    lines = aoc_input().strip().split('\n')
    for l in lines:
        cmd, amount = tokens(l)
        if cmd == "forward":
            x += amount
        elif cmd == "down":
            y += amount
        elif cmd == "up":
            y -= amount

    print(x * y)



def part2():
    x, y, aim = 0, 0, 0
    lines = aoc_input().strip().split('\n')
    for l in lines:
        cmd, amount = tokens(l)
        if cmd == "forward":
            x += amount
            y += amount * aim
        elif cmd == "down":
            aim += amount
        elif cmd == "up":
            aim -= amount

    print(x * y)



if __name__ == "__main__":
    part1()
    part2()
