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



def decompile(prg, ireg):
    regexpr = [0] * 6
    for line, (op, a, b, c) in enumerate(prg):
        trop = f"{op} {a} {b} {c}"
        if op == "seti":
            if c == ireg:
                trop = f"GOTO {a + 1}"
            else:
                trop = f"REG[{c}] = {a}"
        elif op == "bani":
            trop = f"REG[{c}] = REG[{a}] & {b}"
        elif op == "bori":
            trop = f"REG[{c}] = REG[{a}] | {b}"
        elif op == "eqri":
            trop = f"REG[{c}] = REG[{a}] == {b}"
        elif op == "addr":
            if c == ireg and b == ireg:
                trop = f"GOTO {line + 1} + REG[{a}]"
            else:
                trop = f"REG[{c}] = REG[{a}] + REG[{b}]"
        elif op == "muli":
            trop = f"REG[{c}] = REG[{a}] * {b}"
        elif op == "addi":
            if c == ireg and a == ireg:
                trop = f"GOTO {line + 1 + b}"
            else:
                trop = f"REG[{c}] = REG[{a}] + {b}"
        elif op == "setr":
            trop = f"REG[{c}] = REG[{a}]"
        elif op == "eqrr":
            trop = f"REG[{c}] = REG[{a}] == REG[{b}]"
        elif op == "gtir":
            trop = f"REG[{c}] = {a} > REG[{b}]"
        elif op == "gtrr":
            trop = f"REG[{c}] = REG[{a}] > REG[{b}]"
        print(f"{line}: {trop}")


def part1():
    src = aoc_input()
    instrp = ints(lines(src)[0])[0]
    prg = [tokens(l) for l in lines(src)[1:]]
    #decompile(prg, instrp)
    reg = [0] * 6
    used_instr = 0
    while 1:
        nextinstri = reg[instrp]
        if 0 <= nextinstri < len(prg):
            used_instr += 1
            if nextinstri == 28:
                print("ans", reg[5])
                return

            op, *args = prg[nextinstri]
            ops[op](reg, *args)
            reg[instrp] += 1
        else:
            print("exit")
            break


def part2():
    reg = [0] * 6

    # decompiled program:
    reg[5] = 123
    while (reg[5] & 456) != 72:
        pass

    reg[5] = 0
    reg[4] = reg[5] | 0b10000000000000000
    reg[5] = 15466939

    seen = set()
    last = None
    while 1:
        reg[5] += reg[4] & 0b11111111
        reg[5] &= 0b111111111111111111111111
        reg[5] *= 65899
        reg[5] &= 0b111111111111111111111111

        if reg[4] < 256:
            if reg[5] in seen:
                print("ans", last)
                break
            else:
                seen.add(reg[5])
                last = reg[5]

            if reg[5] == reg[0]:
                exit()
            else:
                reg[4] = reg[5] | 0b10000000000000000
                reg[5] = 15466939
                continue

        reg[4] >>= 8   # rewritten from a slow division loop


part1()
part2()
