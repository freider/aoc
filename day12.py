import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input

LEFT = np.array([
    [0, 1],
    [-1, 0]
])

def part1():
    pos = np.array([0, 0])
    direction = np.array([0, 1])
    lines = aoc_input().strip().split('\n')
    for l in lines:
        instr = l[0]
        num = int(l[1:])
        if instr == "L":
            assert num % 90 == 0
            rot = (num // 90) % 4
            for _ in range(rot):
                direction = LEFT @ direction
        elif instr == "R":
            assert num % 90 == 0
            rot = (4 - num // 90) % 4
            for _ in range(rot):
                direction = LEFT @ direction
        elif instr == "N":
            pos += (num, 0)
        elif instr == "S":
            pos += (-num, 0)
        elif instr == "E":
            pos += (0, num)
        elif instr == "W":
            pos += (0, -num)
        elif instr == "F":
            pos += direction * num
        else:
            print("ERROR", instr)
    return np.abs(pos).sum()


def part2():
    wp = np.array([1, 10])
    pos = np.array([0, 0])
    lines = aoc_input().strip().split('\n')
    for l in lines:
        instr = l[0]
        num = int(l[1:])
        if instr == "L":
            assert num % 90 == 0
            rot = (num // 90) % 4
            for _ in range(rot):
                wp = LEFT @ wp
        elif instr == "R":
            assert num % 90 == 0
            rot = (4 - num // 90) % 4
            for _ in range(rot):
                wp = LEFT @ wp
        elif instr == "N":
            wp += (num, 0)
        elif instr == "S":
            wp += (-num, 0)
        elif instr == "E":
            wp += (0, num)
        elif instr == "W":
            wp += (0, -num)
        elif instr == "F":
            pos += wp * num
        else:
            print("ERROR", instr)

    return np.abs(pos).sum()



if __name__ == "__main__":
    print(part1())
    print(part2())

"""
R180
W1
F1
"""