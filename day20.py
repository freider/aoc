from collections import defaultdict, namedtuple
from functools import reduce

import numpy as np
from scipy.ndimage import correlate

from lib.input import aoc_input

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

    alt = defaultdict(list)
    alt_tids = defaultdict(set)
    for tid, t in tiles.items():
        for trans in transforms:
            tt = dotrans(t, trans)
            alt[tuple(tt[0,::])].append((tid, tt))
            alt_tids[tuple(tt[0,::])].add(tid)

    upper_left_id = None
    upper_left = None
    corners = set()
    for tid, t in tiles.items():
        for trans in transforms:
            variant = dotrans(t, trans)
            top = variant[0, ::]
            left = variant[::, 0]
            if len(alt_tids[tuple(top)]) == 1 and len(alt_tids[tuple(left)]) == 1:
                corners.add(tid)
                upper_left_id = tid
                upper_left = variant

    print(reduce(lambda a, b: a*b, corners))  # part 1

    # find layout
    used = {upper_left_id}
    prev = upper_left
    full = [[prev]]

    for it in range(len(tiles) - 1):
        right = prev[::,-1]
        try:
            newi, newt = next((tid, tt) for tid, tt in alt[tuple(right)] if tid not in used)
            # add on right
            newt = newt.T  # alt is indexed by top rows, so transpose to get "left" version
            full[-1].append(newt)
        except StopIteration:  # no match on right side, find start of next row instead
            bottom = full[-1][0][-1,::]
            newi, newt = next((tid, tt) for tid, tt in alt[tuple(bottom)] if tid not in used)
            full.append([newt])

        used.add(newi)
        prev = newt

    # construct image
    img = np.concatenate(
        [np.concatenate(
            [part[1:-1, 1:-1] for part in row],
            axis=1,
        ) for row in full],
        axis=0
    )

    pattern = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    snake = np.array([[1 if c == "#" else 0 for c in l] for l in pattern.split("\n")], dtype=int)
    for t in transforms:
        s = dotrans(snake, t)
        matching_pixels = correlate(img, s, mode='constant') == s.sum()
        if matching_pixels.sum():
            break

    print(img.sum() - matching_pixels.sum() * snake.sum())  #part 2



if __name__ == "__main__":
    both()
