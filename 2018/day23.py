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
import heapq


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
                
def bdist(bounds):
    return min(getdist(p) for p in box_corners(bounds))

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


    q = []
    boxcount = [0]

    def expand(bounds):
        # subdivide bounds into 8 sub cubes
        mid = (bounds[:,0] + bounds[:,1]) // 2
        allbounds = np.stack((bounds[:,0], mid, bounds[:,1]), axis=1)

        for xd in range(2):
            for yd in range(2):
                for zd in range(2):
                    subbox = np.array([allbounds[i, half:half+2] for i, half in enumerate([xd, yd, zd])])
                    size = subbox[:, 1] - subbox[:, 0]
                    if (size <= 0).any():
                        continue
                    num_intersected = sum(1 for _ in get_num_intersects(subbox, oktas))
                    if num_intersected == 0:
                        continue
                    boxdist = bdist(subbox)
                    heapq.heappush(q, (-num_intersected, boxdist, boxcount[0], subbox))
                    boxcount[0] += 1


    q.append((-len(oktas), max_dist, 0, maxbounds))
    boxcount[0] += 1

    while q:
        invint, dist, _, bounds = heapq.heappop(q)
        print(len(q), invint, dist)
        if ((bounds[:, 1] - bounds[:, 0]) == 1).all():
            print("Done", -invint, dist, bounds)
            break
        
        expand(bounds)



if __name__ == "__main__":
    #part1()
    part2()
