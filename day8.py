import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input




def part1():
    lines = aoc_input().strip().split('\n')
    prg = [(instr, int(num)) for instr, num in [x.split() for x in lines]]
    acc = 0
    ix = 0
    visited = set()
    while True:
        instr, num = prg[ix]
        if ix in visited:
            print(acc)
            break
        visited.add(ix)
        if instr == "nop":
            ix += 1
        elif instr == "acc":
            acc += num
            ix += 1
        else:
            ix += num




def part2():
    lines = aoc_input().strip().split('\n')
    _prg = [(instr, int(num)) for instr, num in [x.split() for x in lines]]
    done = False
    for i in range(len(_prg)):
        prg = [x for x in _prg]
        if prg[i][0] == "jmp":
            prg[i] = ("nop", prg[i][1])
        elif prg[i][0] == "nop":
            prg[i] = ("jmp", prg[i][1])
        acc = 0
        ix = 0
        visited = set()
        while True:
            if ix == len(prg):
                print(acc)
                done = True
                break
            instr, num = prg[ix]
            if ix in visited:
                break
            visited.add(ix)
            if instr == "nop":
                ix += 1
            elif instr == "acc":
                acc += num
                ix += 1
            else:
                ix += num




if __name__ == "__main__":
    part1()
    part2()
