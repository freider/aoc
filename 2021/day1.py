import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, ints


def part1():
    nums = [int(x) for x in aoc_input().strip().split('\n')]
    last = nums[0]
    s = 0
    for n in nums[1:]:
        if n > last:
            s += 1
        last = n
    print(s)


def part2():
    nums = [int(x) for x in aoc_input().strip().split('\n')]
    mums = []
    for i in range(len(nums) - 2):
        mums.append(sum(nums[i:i + 3]))

    last = mums[0]
    s = 0
    for n in mums[1:]:
        if n > last:
            s += 1
        last = n
    print(s)


if __name__ == "__main__":
    part1()
    part2()
