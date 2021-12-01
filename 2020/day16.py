from collections import defaultdict

import itertools

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def p2_parse():
    data = aoc_input().strip()
    p1, p2 = data.split("\n\nnearby tickets:\n")
    nts = p2.split("\n")
    rs = p1.split("\n\nyour ticket:\n")[0].split("\n")
    my_ticket = p1.split("\n\nyour ticket:\n")[1]

    rules = []
    named_rules = []
    for r in rs:
        rulename, d = r.split(": ")
        rawranges = d.split(" or ")
        ranges = [[int(x) for x in lohi.split("-")] for lohi in rawranges]
        rules.append(ranges)
        named_rules.append((rulename, ranges))

    valid_tickets = []
    for t in nts:
        nums = [int(x) for x in t.split(",")]
        valids = set()
        for ruleset in rules:
            for r in ruleset:
                for n in nums:
                    if n >= r[0] and n <= r[1]:
                        valids.add(n)
            #v = nums[(nums >= r[0]) | (nums <= r[1])]
            #valids += set(v)
        invalids = set(nums) - set(valids)
        if not invalids:
            valid_tickets.append(t)

    return named_rules, my_ticket, valid_tickets


def part1():
    data = aoc_input().strip()
    p1, p2 = data.split("\n\nnearby tickets:\n")
    nts = p2.split("\n")
    rs = p1.split("\n\nyour ticket:\n")[0].split("\n")
    rules = []
    for r in rs:
        d = r.split(": ")[1]
        rawranges = d.split(" or ")
        ranges = [[int(x) for x in lohi.split("-")] for lohi in rawranges]
        rules.append(ranges)

    tot = 0
    for t in nts:
        nums = [int(x) for x in t.split(",")]
        valids = set()
        for ruleset in rules:
            for r in ruleset:
                for n in nums:
                    if n >= r[0] and n <= r[1]:
                        valids.add(n)
            #v = nums[(nums >= r[0]) | (nums <= r[1])]
            #valids += set(v)
        invalids = set(nums) - set(valids)
        tot += sum(invalids)
    print(tot)



def part2():
    rules, my_t, other_t = p2_parse()
    def pt(t):
        return [int(x) for x in t.split(",")]

    all_t = [pt(x) for x in other_t + [my_t]]
    rulenums = list(range(len(rules)))

    ri_match = defaultdict(list)
    for ri in rulenums:
        conds = rules[ri][1]
        for ti in rulenums:
            for t in all_t:
                if not (conds[0][0] <= t[ti] <= conds[0][1] or conds[1][0] <= t[ti] <= conds[1][1]):
                    break
            else:
                ri_match[ri].append(ti)

    order_map = sorted([(len(matches), ri) for ri, matches in ri_match.items()])

    def do(n, left):
        if n == len(rules):
            yield []

        ri = order_map[n][1]
        for i in left:
            if i in ri_match[ri]:
                for s in do(n + 1, left - {i}):
                    yield [i] + s

    matchup = None
    for s in do(0, set(rulenums)):
        matchup = {order_map[i][1]: s[i] for i in rulenums}
        break

    my_tick = pt(my_t)
    mult = 1
    for i, r in enumerate(rules):
        if r[0].startswith("departure"):
            mult *= my_tick[matchup[i]]
    print(mult)


if __name__ == "__main__":
    part1()
    part2()
