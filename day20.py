from collections import defaultdict, namedtuple, Counter

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul

from scipy.ndimage import correlate

from lib.draw import draw, sparse_to_array
import pyparsing as pp
from lib.input import aoc_input, np_map, pb_input

transform = namedtuple("transform", "trans flipx flipy")
transforms = []
for r in range(2):
    for fx in range(2):
        for fy in range(2):
            transforms.append(transform(r, fx, fy))

def dotrans(t, trans):
    tt = np.copy(t)
    if trans.trans:
        tt = tt.T
    if trans.flipx:
        tt = tt[::-1,::]
    if trans.flipy:
        tt = tt[::,::-1]
    return tt

def both():
    lines = aoc_input().strip()
    raw = lines.split("\n\n")
    tiles = {}
    for r in raw:
        lines = r.split("\n")
        id = int(lines[0].split(" ")[1].strip(":"))
        tile = np.array([[1 if c == "#" else 0 for c in l] for l in lines[1:]], dtype=int)
        tiles[id] = tile

    alt = defaultdict(set)
    for tid, t in tiles.items():
        for trans in transforms:
            tt = dotrans(t, trans)
            alt[tuple(tt[0,::])].add((tid, trans))

    uniq = defaultdict(int)
    for e, comb in alt.items():
        tids = set(x[0] for x in comb)
        if len(tids) == 1:
            uniq[next(iter(tids))] += 1

    #print(uniq)
    m = 1
    corners = []
    for u, l in uniq.items():
        if l == 4:
            corners.append(u)
            m *= u
    print(reduce(lambda a, b: a*b, corners, 1))

    # construct full image
    starting_corner = corners[0]
    used = {starting_corner}
    prev = tiles[starting_corner][::-1,::]  # hack: hardcoded upside down tile based on corner orientation of starting corner
    full = [[prev]]

    for it in range(len(tiles) - 1):
        right = prev[::,-1]
        opts = [(tid, trans) for tid, trans in alt[tuple(right)] if tid not in used]
        if opts:
            n = opts[0]
            newt = dotrans(tiles[n[0]], n[1]).T
            full[-1].append(newt)
        else:
            bottom = full[-1][0][-1,::]  # first of last row
            opts = [(tid, trans) for tid, trans in alt[tuple(bottom)] if tid not in used]
            n = opts[0]
            newt = dotrans(tiles[n[0]], n[1])
            full.append([newt])

        newi = n[0]
        used.add(newi)
        prev = newt

    tileheight, tilewidth = tiles[next(iter(tiles.keys()))].shape
    th = tileheight - 2
    tw = tilewidth - 2
    img = np.zeros((len(full) * th, len(full[0]) * tw), dtype=int)
    for ty, row in enumerate(full):
        for tx, tile in enumerate(row):
            img[ty*th: (ty+1)*th, tx*tw: (tx+1)*tw] = tile[1:-1, 1:-1]

    pattern = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    snake = np.array([[1 if c == "#" else 0 for c in l] for l in pattern.split("\n")], dtype=int)
    for t in transforms:
        s = dotrans(snake, t)
        matching_pixels = correlate(img, s, mode='constant') == s.sum()
        if matching_pixels.sum():
            break

    # Reactivate the following if snakes can overlap (which they can't in the input)
    # px = set()
    # for (y, x), v in np.ndenumerate(matching_pixels):
    #     for (sy, sx), vv in np.ndenumerate(s):
    #         if v == 1 and vv == 1:
    #             p = (y + sy, x + sx)
    #             px.add(p)

    print(img.sum() - matching_pixels.sum() * snake.sum())
    #print(len(px))


if __name__ == "__main__":
    both()
