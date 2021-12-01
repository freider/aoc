from collections import deque

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp
from lib.input import aoc_input, np_map, pb_input


def part1():
    p1, p2 = aoc_input().strip().split('\n\n')
    c1 = deque(int(x) for x in p1.split("\n")[1:])
    c2 = deque(int(x) for x in p2.split("\n")[1:])
    winner = None
    while not winner:
        a = c1.popleft()
        b = c2.popleft()
        if a > b:
            c1.append(a)
            c1.append(b)
        else:
            c2.append(b)
            c2.append(a)
        if len(c1) == 0:
            winner = c2
        elif len(c2) == 0:
            winner = c1

    score = 0
    v = 1
    while winner:
        p = winner.pop()
        score += v * int(p)
        v += 1
    print(score)



def part2():
    p1, p2 = aoc_input().strip().split('\n\n')
    c1 = deque(int(x) for x in p1.split("\n")[1:])
    c2 = deque(int(x) for x in p2.split("\n")[1:])
    mem = {}


    def g(c1, c2, level=0):
        #print("level", level)
        prev = set()
        while True:
            id = (tuple(c1), tuple(c2))
            if id in prev:
                return 1, c1
            #if id in mem:
            #    return mem[id]
            prev.add(id)

            a = c1.popleft()
            b = c2.popleft()

            if a <= len(c1) and b <= len(c2):
                round_winner, _ = g(deque(list(c1)[:a]), deque(list(c2)[:b]), level+1)
            else:
                round_winner = 1 if a > b else 2

            if round_winner == 1:
                c1.append(a)
                c1.append(b)
            elif round_winner == 2:
                c2.append(b)
                c2.append(a)
            else:
                assert False

            if len(c1) == 0:
                mem[id] = (2, c2)
                return 2, c2
            elif len(c2) == 0:
                mem[id] = (1, c1)
                return 1, c1

    score = 0
    v = 1
    _, winner = g(c1, c2)
    while winner:
        p = winner.pop()
        score += v * int(p)
        v += 1
    print(score)



if __name__ == "__main__":
    part1()
    part2()
