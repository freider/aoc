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

from dataclasses import dataclass


class Node:
    def __init__(self, parent, type):
        self.parent = parent
        self.type = type
        self.sub = []

    def print(self, depth=0):
        print(depth * "  " + self.type)
        for s in self.sub:
            s.print(depth+1)


def part1():
    src = """^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"""
    src = aoc_input()
    s = src[1:-1]
    top = Node(None, "seq")
    current = top
    
    for c in s:
        if c in "ESWN":
            current.sub.append(Node(current.sub, c))
        elif c == "(":
            new = Node(current, "opt")
            newseq = Node(new, "seq")
            new.sub.append(newseq)
            current.sub.append(new)
            current = newseq
        elif c == ")":
            current = current.parent.parent
        elif c == "|":
            opt = current.parent
            newseq = Node(opt, "seq")
            opt.sub.append(newseq)
            current = newseq
    #top.print()
    print("parsed")
    dirs = [Point(*p) for p in [(-1, 0), (0, -1), (0, 1), (1, 0)]]
    from networkx import DiGraph

    g = DiGraph()
    
    def rec(n, p):
        if n.type in "NWES":
            dir = dirs["NWES".index(n.type)]
            p1 = p
            # door at p + dir
            p2 = p + (dir * 2)
            g.add_edge(p1, p2)
            print("len", len(g.nodes))
            #print("visiting", p2)
            yield p2
            return

        if n.type == "seq":
            prev = [p]
            for s in n.sub:
                nxt = set()
                for pt in prev:
                    nxt |= set(rec(s, pt))
                prev = nxt
            yield from iter(prev)
            return
        
        if n.type == "opt":
            opts = set()
            for s in n.sub:
                opts |= set(rec(s, p))
            yield from opts
            return
        
        assert False
    import sys
    sys.setrecursionlimit(2000)
    list(rec(top, Point(0, 0)))

    #print(max(len(x) for x in nx.shortest_path(g, source=Point(0, 0)).values()) - 1)
    print(sum(1 for x in nx.shortest_path(g, source=Point(0, 0)).values() if len(x) - 1 >= 1000))


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
