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


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]

def addi(reg, a, b, c):
    reg[c] = reg[a] + b

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]

def muli(reg, a, b, c):
    reg[c] = reg[a] * b

def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]

def bani(reg, a, b, c):
    reg[c] = reg[a] & b

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]

def bori(reg, a, b, c):
    reg[c] = reg[a] | b

def setr(reg, a, b, c):
    reg[c] = reg[a]

def seti(reg, a, b, c):
    reg[c] = a

def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0

def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0

def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0

def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0

def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0

def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0



ops = {n: globals()[n] for n in "addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr".split()}


def part1():
    src = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
    src = aoc_input()
    instrp = ints(lines(src)[0])[0]
    prg = [tokens(l) for l in lines(src)[1:]]
    reg = [0] * 6

    while 1:
        nextinstri = reg[instrp]
        if 0 <= nextinstri < len(prg):
            #print(reg)
            op, *args = prg[nextinstri]
            ops[op](reg, *args)
            #print(reg)
            reg[instrp] += 1
        else:
            break
    print(reg[0])


def part2():
    src = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
    src = aoc_input()
    instrp = ints(lines(src)[0])[0]
    prg = [tokens(l) for l in lines(src)[1:]]
    reg = [0] * 6
    reg[0] = 1
    #reg = [1, 5, 10551305, 3, 10551305//5, 0]
    #reg = [1 + 5 + 17 + 124133 + 10551305, 10551305, 10551305, 3, 10551305, 0]
    #print(1 + 5 + 17 + 124133 + 10551305)
    # seems to add every divisor of 10551305 to reg[0]...
    
    sm = 0
    for div in range(1, 10551306):
        if 10551305 % div == 0:
            print("div", div)
            sm += div
        if sm > 10551305:
            break
    else:
        print("doh")
    print("ans", sm)
    return

    reg = [1, 0, 0, 0, 0, 0]
    reg = [0, 1, 10551305, 3, 1, 10550400] # 3, 4, 5, 6, 8, 9, 10, 11
    reg = [0, 1, 10551305, 3, 10551305, 0]

    reg = [0, 1, 10551305, 3, 10551305, 0]
    #reg = [0, 1, 10551305, 8, 10551304, 0]
    #reg = [1, 2, 10551305, 8, 10551304, 0]
    for i in range(100):
        nextinstri = reg[instrp]
    
        if 0 <= nextinstri < len(prg):
            #print(reg)
            op, *args = prg[nextinstri]
            print(nextinstri, reg, op, args)
            ops[op](reg, *args)
            #print(reg)
            reg[instrp] += 1
        else:
            print("ans", reg[0])
            break

    #  too low: 10675461
    #  too low: 13282317
    

if __name__ == "__main__":
    #part1()
    part2()



"""

reg[5] = reg[1] * reg[4]   # 3

reg[5] = reg[2] == reg[5]  # 4

reg[3] += reg[5] + 1  #  5, 6

reg[4] += 1  # 8

reg[5] = reg[4] > reg[2]  # 9

reg[3] += reg[5] # 10

reg[3] = 2  # 11


---

ptr += (reg[2] == (reg[1] * reg[4])) + 1
reg[4] += 1
ptr += reg[4] > reg[2]
reg[3] = 2




if 10551305 == reg[1] * reg[4]:
    reg[0] += reg[1]

reg[4] += 1

if reg[4] > 10551305:

goto A




loop:
    if reg[1] * reg[4] == 10551305:
        reg[0] += reg[1]
    
    reg[4] += 1

    if reg[4] > 10551305:
        reg[1] += 1
        if reg[1] > reg[2]:
            exit()
        
        reg[4] = 1
"""