import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def part1():
    lines = aoc_input().strip().split(',')
    nums = [int(n) for n in lines]
    print(nums)
    seen = dict()
    last = None
    for i in range(2020):
        if i < len(nums):
            new = nums[i]
        else:
            if last in seen:
                new = i - 1 - seen[last]
            else:
                new = 0

        seen[last] = i - 1
        last = new

    print(last)


def part2():
    lines = aoc_input().strip().split(',')
    nums = [int(n) for n in lines]
    print(nums)
    seen = dict()
    last = None
    for i in range(30000000):
        if i < len(nums):
            new = nums[i]
        else:
            if last in seen:
                new = i - 1 - seen[last]
            else:
                new = 0

        seen[last] = i - 1
        last = new

    print(last)


if __name__ == "__main__":
    part1()
    part2()
