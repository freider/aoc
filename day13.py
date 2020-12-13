from math import gcd, lcm

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def part1():
    lines = aoc_input().strip().split('\n')
    start = int(lines[0])
    busses = [int(l) for l in lines[1].split(",") if l != "x"]

    win = None
    min = None
    for b in busses:
        t = b - start % b
        if min is None or t < min:
            min = t
            win = b
    print(win, min, win * min)


def mod_inverse(a, m):
    if (m == 1):
        return 0

    m0 = m
    y = 0
    x = 1

    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    return (x + m) % m0


def part2():
    lines = aoc_input().strip().split('\n')
    start = int(lines[0])
    busses = [int(l) if l != "x" else 0 for l in lines[1].split(",")]

    prev_period = busses[0]
    prev_offset = 0

    offset = 0
    for b in busses[1:]:
        offset -= 1
        if b == 0:
            continue

        # n * prev_period + prev_offset = m * b - offset
        # n * prev_period + prev_offset + offset = m * b
        new_period = lcm(prev_period, b)
        reps = (mod_inverse(prev_period, b) * (offset - prev_offset)) % b
        new_offset = prev_offset + reps * prev_period
        print("it {} + n * {}".format(new_offset, new_period))

        prev_period = new_period
        prev_offset = new_offset

    print(prev_offset)

"""
939
7,13,x,x,59,x,31,19

# 7n

7 * n % 13 = 12
=> n = 2 * 13 % 13 = 11

Eq => 7 * 11 + (7 * 13)n


77 + 91n % 59 = - 4 = 55

91n % 59 = 37
o=888 => 3

77 + 91 * 3 + 5369n = 

"""





if __name__ == "__main__":
    print(part1())
    print(part2())

