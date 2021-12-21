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
    src = """Player 1 starting position: 4
Player 2 starting position: 8
"""
    src = aoc_input()
    nums = ints(src)
    pos = [nums[1] - 1, nums[3] - 1]
    score = [0, 0]

    print(pos)
    i = 0
    r = 1
    while 1:
        pos[0] = (pos[0] + 3 * r + 3) % 10
        r += 3
        score[0] += pos[0] + 1
        if score[0] >= 1000:
            break

        pos[1] = (pos[1] + 3 * r + 3) % 10
        r += 3
        score[1] += pos[1] + 1
        if score[1] >= 1000:
            break
        i += 1

    print(min(score) * (r - 1))


def part2():
    src = """Player 1 starting position: 4
Player 2 starting position: 8
"""
    src = aoc_input()
    nums = ints(src)
    pos = [nums[1] - 1, nums[3] - 1]
    # outcomes[player][score][pos]
    prev = [
        defaultdict(lambda: defaultdict(int)),
        defaultdict(lambda: defaultdict(int)),
    ]

    prev[0][0][pos[0]] = 1
    prev[1][0][pos[1]] = 1

    wins = [0, 0]

    for turn in range(65):
        player = turn % 2
        other = (player + 1) % 2
        nxt = defaultdict(lambda: defaultdict(int))
        other_outcomes = sum(sum(poss.values()) for poss in prev[other].values())

        for score, poss in prev[player].items():
            for pos, outcomes in poss.items():
                for r1 in range(1, 4):
                    for r2 in range(1, 4):
                        for r3 in range(1, 4):
                            r = r1 + r2 + r3
                            newpos = (pos + r) % 10
                            newscore = score + newpos + 1
                            if newscore >= 21:
                                wins[player] += outcomes * other_outcomes
                            else:
                                nxt[newscore][newpos] += outcomes
        prev[player] = nxt

    print(max(wins))


if __name__ == "__main__":
    part1()
    part2()
