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
    src = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""
    src = aoc_input()
    n = np.array([ints(l) for l in lines(src)])
    strong = np.argmax(n[:, 3])
    print(np.sum((np.sum(np.abs(n[:, :3] - n[strong, :3]), axis=1) <= n[strong, 3]) * 1))


def okta_corners(okta):
    for axis in range(3):
        v = np.zeros((3,))
        v[axis] = 1
        for dir in [-1, 1]:
            yield okta[:3] + (v * dir * okta[3])

def box_corners(bounds):
    inner = bounds.copy()
    inner[:,1] -= 1
    for i in range(2):
        for j in range(2):
            for k in range(2):
                yield np.array([inner[0,i], inner[1, j], inner[2, k]])
                

def part2():
    src = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""


    src = aoc_input()
    oktas = np.array([ints(l) for l in lines(src)]).T
    mins = np.min(oktas - oktas[3], axis=1)
    maxs = np.max(oktas + oktas[3], axis=1) + 1
    oktas = oktas.T
    maxbounds = np.stack((mins, maxs), axis=1)[:3]
    max_dist = np.abs(maxbounds[:, 1]).sum()

    def get_num_intersects(bounds, oktas):
        for okta in oktas:
            for o_corner in okta_corners(okta):
                if (o_corner >= bounds[:, 0]).all() and (o_corner < bounds[:, 1]).all():
                    yield okta
                    break
            else:
                for b_corner in box_corners(bounds):
                    if np.abs(okta[:3] - b_corner).sum() <= okta[3]:
                        yield okta
                        break

    def getdist(p):
        return np.abs(p).sum()

    def bestpoint(nint, bounds, closer_than, oktas):
        size = bounds[:, 1] - bounds[:, 0]
        if (size <= 0).any():
            return None, None
        
        intersected = list(get_num_intersects(bounds, oktas))
        if len(intersected) < nint:
            return None, None
    
        if (size == 1).all():
            print(bounds[:,0], closer_than, nint, len(oktas), min(getdist(p) for p in box_corners(bounds)))
            p = bounds[:,0]
            return getdist(p), p
        
        # subdivide bounds into 8 sub cubes
        subboxes = []
        mid = (bounds[:,0] + bounds[:,1]) // 2
        allbounds = np.stack((bounds[:,0], mid, bounds[:,1]), axis=1)

        for xd in range(2):
            for yd in range(2):
                for zd in range(2):
                    subbox = np.array([allbounds[i, half:half+2] for i, half in enumerate([xd, yd, zd])])
                    boxdist = min(getdist(p) for p in box_corners(subbox))
                    subboxes.append((boxdist, len(subboxes), subbox))

        best_dist = closer_than
        best_p = None
        for boxdist, _, subbox in sorted(subboxes):
            if boxdist >= best_dist:
                continue
            dist, p = bestpoint(nint, subbox, best_dist, intersected)
            if p is not None:
                if dist < best_dist:
                    best_dist = dist
                    best_p = p
        return best_dist, best_p

    lb = 0 # tested to work
    ub = len(oktas) + 1 # tested to not work
    while lb < ub - 1:
        t = (ub + lb + 1) // 2
        d, p = bestpoint(t, maxbounds, max_dist, oktas)
        print(t, d, p)
        if p is None:
            # lower the bound
            ub = t
        else:
            lb = t

    print("num overlaps", lb)
    print(bestpoint(lb, maxbounds, max_dist))



if __name__ == "__main__":
    #part1()
    part2()
