import numpy as np
from scipy import ndimage

from lib.input import aoc_input, ints
from lib.point import Point

serial = ints(aoc_input())[0]
pic = np.zeros((300, 300), dtype=int)

def pwr(x, y):
    rack_id = x + 10
    pwr = rack_id * y
    pwr += serial
    pwr *= rack_id
    pwr = (pwr % 1000) // 100
    pwr -= 5
    return pwr


for (y, x), p in np.ndenumerate(pic):
    pic[y, x] = pwr(x+1, y+1)

corr = ndimage.correlate(pic, np.ones((3, 3)), mode='constant', cval=0)
print(",".join(reversed([str(x) for x in np.unravel_index(np.argmax(corr), corr.shape)])))


def f():
    cumsums = np.pad(np.cumsum(np.cumsum(pic, axis=1), axis=0), 1, constant_values=0)
    for p in Point.range(Point(0, 0), Point(299, 299)):
        maxs = min(p.np())
        for s in range(1, maxs + 1):
            yield cumsums[p[1], p[0]] + cumsums[p[1]-s, p[0]-s] - cumsums[p[1]-s, p[0]] - cumsums[p[1], p[0]-s], f"{p[0] - s + 1},{p[1] - s + 1},{s}"

print(max(f()))
