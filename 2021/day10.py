import sys
import re
from collections import Counter, defaultdict, deque

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    src = aoc_input()

    pairs = [
        "[]",
        "{}",
        "<>",
        "()"
    ]
    closers = dict((b, a) for a, b in pairs)

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    score = 0
    for line in lines(src):
        d = deque([])

        for c in line:
            if c in closers:
                opener = closers[c]
                if len(d) == 0 or d.pop() != opener:
                    print("illegal", c)
                    score += scores[c]
                    break
            else:
                d.append(c)


    print(score)



def part2():
    src = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    src = aoc_input()

    pairs = [
        "[]",
        "{}",
        "<>",
        "()"
    ]
    closers = dict((b, a) for a, b in pairs)

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    ac_score = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }
    score = 0
    p2scores = []
    for line in lines(src):
        d = deque([])

        for c in line:
            if c in closers:
                opener = closers[c]
                if len(d) == 0 or d.pop() != opener:
                    score += scores[c]
                    break
            else:
                d.append(c)
        else:
            p2score = 0
            while d:
                c = d.pop()
                p2score = p2score * 5 + ac_score[c]
            p2scores.append(p2score)
    p2scores.sort()
    print(p2scores[len(p2scores) // 2])


if __name__ == "__main__":
    part1()
    part2()
