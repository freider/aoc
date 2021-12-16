"""
Numpy-like dict additions for per-key arithmetics
"""
import pytest


class numdict(dict):
    def __add__(self, other):
        return numdict((key, self.get(key, 0) + other.get(key, 0)) for key in set(self.keys()) | set(other.keys()))

    def __mul__(self, other):
        if isinstance(other, dict):
            # element wise multiplication
            return numdict((key, self.get(key, 0) * other.get(key, 0)) for key in set(self.keys()) | set(other.keys()))
        else:
            # scalar multiplication
            return numdict((key, val * other) for key, val in self.items())

    def __hash__(self):
        # take care when using this as a dict key since the numdict is mutable
        return hash(sorted(self.items()))

@pytest.mark.parametrize(['a', 'b', 'expected'], [
    ({'a': 1}, {'a': 2}, {'a': 3}),
    ({'a': 1}, {'b': 2}, {'a': 1, 'b': 2})
])
def test__addition(a, b, expected):
    assert numdict(a) + numdict(b) == expected


@pytest.mark.parametrize(['a', 'b', 'expected'], [
    ({'a': 3}, {'a': 2}, {'a': 6}),
    ({'a': 1}, {'b': 2}, {'a': 0, 'b': 0}),
    ({'a': 2}, 4, {'a': 8})
])
def test__multiplication(a, b, expected):
    assert numdict(a) * b == expected
