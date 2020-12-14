from math import gcd, lcm

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def tobinstr(v):
    b = []
    while v:
        b.append(str(v % 2))
        v //= 2
    b += (36 - len(b)) * ["0"]
    return "".join(reversed(b))


def part1():
    lines = aoc_input().strip().split('\n')
    mask = None
    mem = {}
    for line in lines:
        if line.startswith("mask"):
            _, mask = line.split(" = ")
        else:
            mo = re.match(r"mem\[(\d+)\] = (\d+)", line)
            loc, val = mo.groups()
            v = int(val)
            bin = tobinstr(v)
            comb = []
            for m, b in zip(mask, bin):
                if m == "X":
                    comb.append(b)
                else:
                    comb.append(m)
            mem[loc] = int("".join(comb), 2)

    print(sum(mem.values()))


def all_addr(m_loc):
    if not m_loc:
        yield ""
        return
    c = m_loc[0]

    if c == "X":
        for sub in all_addr(m_loc[1:]):
            yield "1" + sub
            yield "0" + sub
    else:
        for sub in all_addr(m_loc[1:]):
            yield c + sub

def part2():
    lines = aoc_input().strip().split('\n')
    mask = None
    mem = {}

    instr = []
    for line in lines:
        if line.startswith("mask"):
            _, mask = line.split(" = ")
        else:
            mo = re.match(r"mem\[(\d+)\] = (\d+)", line)
            loc, val = mo.groups()
            bin = tobinstr(int(loc))
            comb = []
            for m, b in zip(mask, bin):
                if m == "0":
                    comb.append(b)
                else:
                    comb.append(m)
            masked_loc = "".join(comb)
            instr.append((masked_loc, int(val)))

    for i, (m_loc, val) in enumerate(instr):
        #print("instr", i)
        for addr in all_addr(m_loc):
            mem[addr] = val

    return sum(mem.values())


if __name__ == "__main__":
    #print(tobinstr(4))
    print(part1())
    print(part2())

