import itertools
import numpy as np
from itertools import count
from scipy.ndimage import convolve, correlate

from lib.input import aoc_input, np_map

dirs = np.array(list(set(itertools.product([-1, 0, 1], [-1, 0, 1])) - {(0, 0)}))


def one_iter(m):
    out = np.empty_like(m, dtype=str)
    for (y, x), v in np.ndenumerate(m):
        loc = np.array([y, x])
        ocount = 0
        for d in dirs:
            p = loc + d
            if ((p >= 0) & (p < m.shape)).all():
                ocount += m[p[0], p[1]] == "#"

        if v == "#" and ocount >= 4:
            out[y, x] = "L"
        elif v == "L" and ocount == 0:
            out[y, x] = "#"
        else:
            out[y, x] = v
    return out


def one_iter_numpy_pix(m):
    out = np.empty_like(m, dtype=str)
    for (y, x), v in np.ndenumerate(m):
        pos = (y, x) + dirs
        adj_pix = pos[((pos < m.shape) & (pos >= 0)).all(axis=1)].T
        ocount = (m[adj_pix[0], adj_pix[1]] == "#").sum()

        if v == "#" and ocount >= 4:
            out[y, x] = "L"
        elif v == "L" and ocount == 0:
            out[y, x] = "#"
        else:
            out[y, x] = v
    return out


def one_iter_numpy(m: np.array):
    adj_taken = correlate(
        (m == "#") * 1,
        [[1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]],
        mode='constant'
    )
    res = m.copy()
    res[(m == "L") & (adj_taken == 0)] = "#"
    res[(m == "#") & (adj_taken >= 4)] = "L"
    return res


def part1():
    m = np_map(aoc_input().strip())
    while 1:
        out = one_iter_numpy(m)
        if (m == out).all():
            break
        m = out
    return np.sum(m == "#")


def one_iter_p2(m):
    out = np.empty_like(m, dtype=str)
    for (y, x), v in np.ndenumerate(m):
        loc = np.array([y, x])
        ocount = 0
        for d in dirs:
            for n in count(1):
                p = loc + d * n
                if ((p >= 0) & (p < m.shape)).all():
                    if m[p[0], p[1]] == "#":
                        ocount += 1
                        break
                    if m[p[0], p[1]] == "L":
                        break
                else:
                    break

        if v == "#" and ocount >= 5:
            out[y, x] = "L"
        elif v == "L" and ocount == 0:
            out[y, x] = "#"
        else:
            out[y, x] = v
    return out


def part2():
    m = np_map(aoc_input().strip())
    while 1:
        out = one_iter_p2(m)
        if (m == out).all():
            break
        m = out
    return np.sum(m == "#")




if __name__ == "__main__":
    print(part1())
    # print(part2())
