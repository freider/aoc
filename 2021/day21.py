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

    # at most 6 rolls

    # mem[score1][score2][rolls][pos1][pos2] = num outcomes

    mem = np.zeros((31, 31, 200, 10, 10), dtype=np.int64)

    mem -= 1
    mem[(0, 0, 0, pos[0], pos[1])] = 1

    def outcomes(score1, score2, rolls, pos1, pos2):
        if score1 < 0 or score2 < 0 or rolls < 0:
            return 0
        cached = mem[(score1, score2, rolls, pos1, pos2)]
        if cached != -1:
            return cached

        oc = 0
        p = ((rolls - 1) // 3) % 2  # current player
        didadjustscore = rolls % 3 == 0
        if p == 0:
            # player 1 makes roll `rolls`
            for res in range(1, 4):
                prev_pos1 = (10 + pos1 - res) % 10
                prev_score1 = score1 - (pos1 + 1) if didadjustscore else score1
                if prev_score1 < 21:
                    oc += outcomes(prev_score1, score2, rolls - 1, prev_pos1, pos2)
        else:
            # player 2 makes roll `rolls`
            for res in range(1, 4):
                prev_pos2 = (10 + pos2 - res) % 10
                prev_score2 = score2 - (pos2 + 1) if didadjustscore else score2
                if prev_score2 < 21:
                    oc += outcomes(score1, prev_score2, rolls - 1, pos1, prev_pos2)
        mem[(score1, score2, rolls, pos1, pos2)] = oc
        return oc

    #return
    wins1 = 0
    wins2 = 0

    # wins for p1
    for s1 in range(21, 31):
        for s2 in range(s1):
            if s2 >= 21:
                continue
            for n in range(15):
                # win for p1:
                r1 = 3 * n + 3
                r2 = 3 * n
                rolls = r1 + r2
                for p1 in range(10):
                    for p2 in range(10):
                        wins1 += outcomes(s1, s2, rolls, p1, p2)

    # wins for p2
    for s2 in range(21, 31):
        for s1 in range(s2):
            if s1 >= 21:
                continue
            for n in range(15):
                # win for p2:
                r1 = 3 * n
                r2 = 3 * n
                rolls = r1 + r2
                for p1 in range(10):
                    for p2 in range(10):
                        wins2 += outcomes(s1, s2, rolls, p1, p2)

    print(wins1, wins2)

    # WA - too high: 1995514900116635


if __name__ == "__main__":
    part1()
    part2()
