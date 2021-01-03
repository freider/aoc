from itertools import count

from lib.input import aoc_input, lines, ints, pb_input
import numpy as np

ar = np.array([ints(l) for l in lines(aoc_input())])


def display(ps):
    origin = ps.min(axis=0)
    size = ps.max(axis=0) - origin
    pic = np.zeros((size[1]+1, size[0]+1))
    for p in ps:
        coord = p - origin
        pic[coord[1], coord[0]] = 1
    for row in pic:
        print("".join(["#" if x else " " for x in row]))


last = None
last_ps = None

for it in count(0):
    ar[:,:2] += ar[:,2:]
    ps = ar[:, :2]
    diff = ps.max(axis=0) - ps.min(axis=0)
    spread = abs(diff[1])

    if last is None or spread < last:
        last = spread
        last_ps = ps.copy()
    else:
        print(it, "seconds")
        display(last_ps)
        break
