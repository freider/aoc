import sys
import re
import numpy as np
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input
from networkx import DiGraph, all_shortest_paths, descendants


def part1():
    lines = aoc_input().strip().split('\n')

    g = DiGraph()
    for l in lines:
        p1, p2 = l.split(" contain ")
        outer = p1.strip()[:-1]
        if "no other bags" in p2:
            continue
        for s in p2.split(", "):
            _num, inner = s.split(" ", 1)
            num = int(_num)
            inner = inner.strip(".")
            if inner.endswith("s"):
                inner = inner[:-1]
            g.add_edge(inner, outer)
    d = descendants(g, source="shiny gold bag")
    print(len(d))


def part2():
    lines = aoc_input().strip().split('\n')

    g = {}
    for l in lines:
        p1, p2 = l.split(" contain ")
        outer = p1.strip()[:-1]
        for s in p2.split(", "):
            if "no other bags" in p2:
                continue
            _num, inner = s.split(" ", 1)
            num = int(_num)
            inner = inner.strip(".")
            if inner.endswith("s"):
                inner = inner[:-1]

            g.setdefault(outer, []).append((num, inner))

    vis = {}

    def rec(cur):
        if cur in vis:
            return vis[cur]

        s = 1
        for (num, e) in g.get(cur, []):
            s += num * rec(e)
        vis[cur] = s
        return s

    print(rec("shiny gold bag") - 1)


if __name__ == "__main__":
    part1()
    part2()
