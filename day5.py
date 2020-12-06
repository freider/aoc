import sys
import re
import numpy as np
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def part1():
    lines = aoc_input().strip().split('\n')
    #nums = [int("".join("1" if c in "BR" else "0" for c in l), 2) for l in lines]
    #nums = [int("".join(str(int(c in "BR")) for c in l), 2) for l in lines]
    nums = [reduce(lambda a, c: a * 2 + (c in 'BR'), l, 0) for l in lines]
    reduce(lambda a, c: a * 2 + (c in 'BR'), l, 0)
    print(max(nums))



def part2():
    lines = aoc_input().strip().split('\n')
    nums = [int("".join("1" if c in "BR" else "0" for c in l), 2) for l in lines]
    for n in range(max(nums) + 1):
        if n not in nums and n + 1 in nums and n - 1 in nums:
            print(n)


if __name__ == "__main__":
    part1()
    part2()
