import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul

from scipy import ndimage

from lib.draw import sparse_to_array
from lib.input import aoc_input, np_map, pb_input

def draw(m):
    for lay in m:
        if lay.sum() > 0:
            print()
            for line in lay:
                print("".join(str(c) for c in line))

def part1():
    N = 6
    lines = aoc_input().strip().split('\n')
    offset = N
    dim = len(lines) + 2 * N
    cube = np.zeros((dim, dim, dim), dtype=int)
    for j, l in enumerate(lines):
        for i, c in enumerate(l.strip()):
            if c == "#":
                cube[offset, offset + j, offset + i] = 1

    weights = np.ones((3, 3, 3))
    weights[1, 1, 1] = 0
    for i in range(N):
        neighbours = ndimage.convolve(
            cube, weights, mode="constant"
        )
        for (a, b, c), v in np.ndenumerate(cube):
            if v == 1:
                if not 2 <= neighbours[a, b, c] <= 3:
                    cube[a, b, c] = 0
            elif neighbours[a, b, c] == 3:
                cube[a, b, c] = 1

    print(cube.sum())


def part2():
    N = 6
    lines = aoc_input().strip().split('\n')
    dim = len(lines) + 2 * N
    cube = np.zeros((dim, dim, dim, dim), dtype=int)
    cube[N, N] = np.pad(np.array([[1 if c == "#" else 0 for c in l] for l in lines]), N)

    weights = np.ones((3, 3, 3, 3))
    weights[1, 1, 1, 1] = 0
    for i in range(N):
        neighbours = ndimage.convolve(
            cube, weights, mode="constant"
        )
        oldcube = np.copy(cube)
        cube[(oldcube == 1) & ((neighbours < 2) | (neighbours > 3))] = 0
        cube[(oldcube == 0) & (neighbours == 3)] = 1

    print(cube.sum())


if __name__ == "__main__":
    part1()
    part2()
