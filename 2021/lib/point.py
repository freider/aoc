import numbers
from typing import Union

import numpy as np
import pytest


# rotates a coordinate (y, x) clockwise in an y/x coordinate system where y points up and x points right
mat_rot90 = np.array([
    [0, -1],
    [1, 0]
])


class Point:
    # hashable point type of any dimension with integer values only
    v: np.array

    @classmethod
    def box_points(cls, p1, p2, inclusive=True):
        """Yield all points in bounded by the p1 <-> p2 box

        * Works for any number of dimensions of p
        * p1 needs to be <= p2 for all dimensions for any points to be generated
        """
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
    def line_points(cls, p1, p2, inclusive=True):
        """Yield all consecutive points on the vertical, horizontal or diagonal line from p1 to p2

        * "Order" of points doesn't matter, i.e. p2 < p1 for any dimensions are fine
        """

        diff = p2 - p1
        assert np.any(np.equal(p1.v, p2.v)) or abs(diff[0]) == abs(diff[1]), "Only straight or diagonal supported"

        steps = np.max(np.abs(diff.v))
        diff = Point(*(diff.v // steps))
        p = p1
        for _ in range(steps + int(inclusive)):
            yield p
            p += diff

    def __iter__(self):
        yield from self.v

    def restrict(self, mincap:'Point' = None, maxcap:'Point' = None):
        mincap = mincap or self.dim * [None]
        maxcap = maxcap or self.dim * [None]

        def minmax(a, b, c):
            if b is not None:
                a = max(a, b)
            if c is not None:
                a = min(a, c)
            return a

        return Point(*(minmax(*c) for c in zip(self.v, mincap, maxcap)))

    def neighbours(self, mincap=None, maxcap=None, distance=1):
        """Get all points within offset distance (default 1)
        * includes the point itself
        * optionally cap the output by mincap and maxcap
        """
        offset = Point(*([distance] * self.dim))
        return Point.box_points(
            (self - offset).restrict(mincap, maxcap),
            (self + offset).restrict(mincap, maxcap)
        )

    def __init__(self, *args):
        assert isinstance(args[0], numbers.Number)
        self.v = np.array(args, dtype=int)

    def __add__(self, other):
        return Point(*(self.v + other.v))

    def __sub__(self, other):
        return Point(*(self.v - other.v))

    def dot(self, other):
        return np.dot(self.v, other.v)

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

    def __lt__(self, other):
        return tuple(self.np()) < tuple(other.np())


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
    assert list(Point.box_points(Point(*a), Point(*b))) == [Point(*p) for p in expected]


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


@pytest.mark.parametrize(
    ["p1", "p2", "inclusive", "expected"],
    [
        [(0, 0), (0, 3), True, [(0, 0), (0, 1), (0, 2), (0, 3)]],
        [(3, 0), (0, 0), True, [(3, 0), (2, 0), (1, 0), (0, 0)]],
        [(-1, 2), (1, 0), False, [(-1, 2), (0, 1)]]
    ]
)
def test__line_points(p1, p2, inclusive, expected):
    res = Point.line_points(Point(*p1), Point(*p2), inclusive=inclusive)
    assert [Point(*p) for p in expected] == list(res)


def test__neighbours():
    assert list(Point(2, 2).neighbours()) == [
        Point(y, x) for y, x in [
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
            (3, 1), (3, 2), (3, 3)
        ]
    ]

    assert list(Point(2, 2).neighbours(maxcap=Point(2, 3))) == [
        Point(y, x) for y, x in [
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
        ]
    ]


@pytest.mark.parametrize(
    ["p1", "p2", "expected"],
    [
        [(1, 3), (2, 7), (3, 10)],
        [(1, 7, -2), (0, 2, 9), (1, 9, 7)],
    ]
)
def test__add(p1, p2, expected):
    assert Point(*p1) + Point(*p2) == Point(*expected)


def test__fail_on_init_array():
    try:
        Point([1, 2])
    except:
        pass
    else:
        assert False, "did not raise"

    try:
        Point(np.array([1.0, 2.0]))
    except:
        pass
    else:
        assert False, "did not raise"
