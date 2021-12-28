import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints, lines
from lib.point import Point


def part1():
    src = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
    src = aoc_input()


    g = nx.DiGraph()
    for l in lines(src):
        c = l.split(" bags")[0]
        content = l.split("contain ")[1][:-1].split(", ")
        for sub in content:
            tok = tokens(sub)
            n = tok[0]
            name = ' '.join(tok[1:-1])

            if n != "no":
                g.add_edge(c, name, num=n)

    print(len(nx.descendants(g.reverse(), "shiny gold")))

    def rec(node, num):
        s = num
        for subnode, data in g[node].items():
            subnum = data['num']
            s += rec(subnode, num * subnum)
        return s

    print(rec("shiny gold", 1) - 1)



def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
