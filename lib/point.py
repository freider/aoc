from typing import Union

import numpy as np
import pytest


# rotates a coordinate (y, x) clockwise in an y/x coordinate system where y points up and x points right
mat_rot90 = np.array([
    [0, -1],
    [1, 0]
])


class Point:
    # hashable point type of any dimension
    v: np.array

    @classmethod
    def range(cls, p1, p2, inclusive=True):
        assert p1.dim == p2.dim
        dim = p1.dim

        def rec(d):
            if d == dim:
                yield ()
                return
            for p in range(p1[d], p2[d] + int(inclusive)):
                subs = rec(d+1)
                for sub in subs:
                    yield (p,) + sub
        return (Point(*p) for p in rec(0))

    @classmethod
    def border_range(cls, p1, p2, inclusive=True):
        p1.v

    def __iter__(self):
        yield from self.v

    def restrict(self, mincap:Union['Point', None] = None, maxcap:Union['Point', None] = None):
        mincap = mincap or self.dim * [None]
        maxcap = maxcap or self.dim * [None]

        def minmax(a, b, c):
            if b is not None:
                a = max(a, b)
            if c is not None:
                a = min(a, c)
            return a

        return Point(*(minmax(*c) for c in zip(self.v, mincap, maxcap)))

    def neighbours(self, mincap=None, maxcap=None):
        offset = Point(*[1] * self.dim)
        return Point.range(
            (self - offset).restrict(mincap, maxcap),
            (self + offset).restrict(mincap, maxcap)
        )

    def __init__(self, *args):
        self.v = np.array(args, dtype=int)

    def __add__(self, other):
        return Point(*(a + b for a, b in zip(self.v, other.v)))

    def __sub__(self, other):
        return Point(*(a - b for a, b in zip(self.v, other.v)))

    def dot(self, other):
        return sum(*(a * b for a, b in zip(self.v, other.v)))

    def np(self):
        return self.v

    def __repr__(self):
        d = ", ".join(str(x) for x in self.v)
        return f"Point({d})"

    def __hash__(self):
        return hash(tuple(self.v))

    def __getitem__(self, item: int):
        return self.v[item]

    @property
    def dim(self):
        return len(self.v)

    def rot90(self, k=1):
        # rotates the XY plane clockwise, assuming coordinates are [y, x] in v
        assert self.dim == 2
        v = self.np()
        for i in range(k % 4):
            v = mat_rot90 @ v
        return Point(*v)

    def __eq__(self, other):
        return self.dim == other.dim and all(a == b for a, b in zip(self.v, other.v))


@pytest.mark.parametrize(
    ["v", "expected"],
    [
        ((1, 0), (0, 1)),
        ((0, 1), (-1, 0)),
        ((-1, 0), (0, -1)),
        ((0, -1), (1, 0)),
        ((1, 1), (-1, 1)),
    ]
)
def test__rot90(v, expected):
    assert Point(*v).rot90() == Point(*expected)


@pytest.mark.parametrize(
    ["a", "b", "expected"],
    [
        ((0, 2), (2, 3), [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]),
        ((0, 0, 0), (1, 1, 1), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]),
    ]
)
def test__range(a, b, expected):
    assert list(Point.range(Point(*a), Point(*b))) == [Point(*p) for p in expected]


@pytest.mark.parametrize(
    ["p", "mincap", "maxcap", "expected"],
    [
        [(-1, 3), (0, 0), None, (0, 3)],
        [(-1, 3), (1, 0), (2, 2), (1, 2)]
    ]
)
def test__restrict(p, mincap, maxcap, expected):
    assert Point(*p).restrict(
        Point(*mincap) if mincap else None,
        Point(*maxcap) if maxcap else None
    ) == Point(*expected)
