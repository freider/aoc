import sys
import re
from collections import Counter, defaultdict
from itertools import permutations

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = aoc_input()
    s = 0
    for l in lines(src):
        pre, post = l.split(" | ")
        outputs = post.split()
        s += sum(1 for c in outputs if len(c) in (2, 4, 3, 7))

    print(s)

chars = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg"
]

def part2():
    src = aoc_input()
    nums = []
    for line in lines(src):
        pre, post = line.split(" | ")
        sigs = pre.split()
        sigset = set(''.join(sorted(w)) for w in sigs)

        for p in permutations("abcdefg"):
            def remap_c(c):
                return p[ord(c) - ord('a')]

            remapped = []
            for word in chars:
                remapped.append(''.join(sorted(remap_c(c) for c in word)))

            if set(remapped) == sigset:
                digs = [''.join(sorted(w)) for w in post.split()]
                num = int(''.join(str(remapped.index(d)) for d in digs))
                nums.append(num)
                break
    print(sum(nums))


def part2_opt():
    def trans(count_set, output_set):
        cnt = Counter(''.join(count_set))
        return [tuple(sorted(cnt[c] for c in w)) for w in output_set]

    trans_to_num = dict(zip(trans(chars, chars), range(10)))
    s = 0
    for line in lines(aoc_input()):
        signals, outputs = line.split(' | ')
        trans_outputs = trans(signals.split(), outputs.split())
        num = int(''.join(str(trans_to_num[op]) for op in trans_outputs))
        s += num
    print(s)


if __name__ == "__main__":
    part1()
    part2()
    part2_opt()
