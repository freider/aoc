import sys
import re
from collections import Counter, defaultdict, deque

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    #
    src = aoc_input()
    obst = set()
    for line in lines(src):
        toks = tokens(line)
        if toks[0] == "x":
            x = toks[1]
            y1, y2 = toks[3:]
            obst |= set(Point.line_points(Point(y1, x), Point(y2, x)))
        else:
            assert toks[0] == "y"
            y = toks[1]
            x1, x2 = toks[3:]
            obst |= set(Point.line_points(Point(y, x1), Point(y, x2)))
    miny = min(o[0] for o in obst)
    maxy = max(o[0] for o in obst)
    water = set()
    everblue = set()
    
    def drawpil():
        minx = min(o[1] for o in obst | water)
        maxx = max(o[1] for o in obst | water)
        miny = min(o[0] for o in obst | water)
        maxy = max(o[0] for o in obst | water)

        from PIL import Image, ImageDraw

        img = Image.new('RGB', (maxx - minx + 1, maxy - miny + 1), color='white')
        d = ImageDraw.Draw(img)
        for p in obst:
            d.point((p[1] - minx, p[0] - miny), "red")
        
        for p in water:
            d.point((p[1] - minx, p[0] - miny), "blue" if p in everblue else "green")

        from tempfile import NamedTemporaryFile
        tfile = NamedTemporaryFile(suffix=".PNG")
        img.save(tfile)
        print(tfile.name)
        input()

    def draw():
        minx = min(p[1] for p in obst)
        maxx = max(p[1] for p in obst)
        for y in range(0, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                p = Point(y, x)
                c = "."
                if p in obst:
                    c = '#'
                elif p in everblue:
                    c = '~'
                elif p in water:
                    c = '|'
                row.append(c)
            print(''.join(row))
        print()

    def flowdown(p):
        while 1:
            water.add(p)
            point_below = p + Point(1, 0)
            if point_below[0] > maxy:
                break

            blocked_below = point_below in obst
            if not blocked_below:
                p = point_below
                continue
            
            while 1:
                blocked_left = flowh(p, Point(0, -1))
                blocked_right = flowh(p, Point(0, 1))
                if blocked_left and blocked_right:
                    flowh(p, Point(0, -1), True)
                    flowh(p, Point(0, 1), True)
                    p = p + Point(-1, 0)
                else:
                    break
            break

    def flowh(p, dir, mark=False):
        while 1:
            water.add(p)
            if mark:
                everblue.add(p)
            point_below = p + Point(1, 0)
            blocked_below = point_below in obst or point_below in everblue

            if not mark and not blocked_below:
                if not point_below in water:
                    flowdown(point_below)
                return False

            p = p + dir
            blocked_next = p in obst
            if blocked_next:
                return True


    source = (Point(0, 500))
    flowdown(source)
    print(min(p[0] for p in water))
    #drawpil()
    print(sum(1 for p in water if p[0] >= miny)) # toohigh: 38453
    print(len(everblue))

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
