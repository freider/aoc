import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def issumof(v, n):
    for i, x in enumerate(v):
        if n - x in v:
            return True
    return False

preamble = 25


def part1():
    lines = aoc_input().strip().split('\n')
    nums = [int(n) for n in lines]

    for i in range(len(nums) - (preamble + 1)):
        v = nums[i:i+preamble]
        c = nums[i+preamble]
        if not issumof(v, c):
            return c

def part2():
    lines = aoc_input().strip().split('\n')
    nums = [int(n) for n in lines]
    p1 = part1()
    cumsum = 0
    cs = []
    for x in nums:
        cumsum += x
        cs.append(cumsum)

    e = set()
    for x in cs:
        if x - p1 in e:
            j = cs.index(x)
            i = cs.index(x - p1)

            return min(nums[i:j+1]) + max(nums[i:j+1])

        e.add(x)


if __name__ == "__main__":
    a = np.array([5, 10, 25, 30])
    ix = np.arange(2)
    print(ix[None:] + ix[:None])
    #print(part1())
    #print(part2())
