import re
import networkx as nx
from lib.input import aoc_input


def part1():
    lines = aoc_input().strip().split('\n')

    g = nx.DiGraph()
    for l in lines:
        if "contain no other" in l:
            continue
        ms = list(re.finditer(r"(\d+)? ?([^\d]+?) bag", l))
        outer = ms[0].group(2)
        for m in ms[1:]:
            inner = m.group(2)
            g.add_edge(inner, outer)

    d = nx.descendants(g, source="shiny gold")
    print(len(d))


def part2():
    lines = aoc_input().strip().split('\n')

    g = nx.DiGraph()
    for l in lines:
        if "contain no other" in l:
            continue
        ms = list(re.finditer(r"(\d+)? ?([^\d]+?) bag", l))
        outer = ms[0].group(2)
        for m in ms[1:]:
            num = int(m.group(1))
            inner = m.group(2)
            g.add_edge(outer, inner, num=num)

    vis = {}

    def rec(cur):
        if cur in vis:
            return vis[cur]

        s = 1 + sum(data["num"] * rec(e) for e, data in g[cur].items())
        vis[cur] = s
        return s

    print(rec("shiny gold") - 1)


if __name__ == "__main__":
    part1()
    part2()
