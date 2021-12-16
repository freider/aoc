import os
import re
import subprocess
from typing import Union
import numpy as np
import pytest
import sys

from lib.aoc_api import Aoc


def infer_day(fn):
    return re.search(r'day([\d]+)', fn).group(1)


def infer_year(fn):
    return re.findall(r'20[\d]{2}', fn)[-1]


def infer_input_dir(fn):
    return os.path.join(os.path.dirname(fn), "inputs")


def pb_input():
    return subprocess.check_output('pbpaste', encoding='utf8')


def aoc_input(fn: Union[str, int, None] = None, year=None, nostrip=False) -> object:
    script_fn = os.path.abspath(sys.argv[0])
    input_fn = infer_day(script_fn) if fn is None else fn
    year = infer_year(script_fn) if year is None else year

    input_dir = infer_input_dir(script_fn)
    relpath = f"{input_dir}/{input_fn}"

    def filecached():
        if os.path.exists(relpath):
            with open(relpath) as f:
                return f.read()
        else:
            if not str(input_fn).isdigit():
                raise Exception("Can only fetch full day input")
            day = input_fn
            txt = Aoc().fetch_input(year, day)
            os.makedirs(input_dir, exist_ok=True)
            with open(relpath, 'w') as f:
                f.write(txt)
            return txt

    d = filecached()
    if nostrip:
        return d
    else:
        return d.rstrip("\n")


def ints(s, negative=True):
    return [int(x) for x in re.findall(r"[+" + (r"\-" if negative else "") + "]?[0-9]+", s)]

def chunks(s):
    return s.split("\n\n")

def lines(s):
    return s.split("\n")

def test__ints():
    assert ints("hej23#-2.5") == [23, -2, 5]


def tokens(s, intify=True, negative=False):
    pat = r"(\w+|{}\d+)".format('-' if negative else '')
    raw = re.findall(pat, s)
    if intify:
        return tuple(int(x) if (x.isdigit() or (negative and x[0] == '-' and x[1:].isdigit())) else x for x in raw)
    return tuple(raw)


@pytest.mark.parametrize(
    ["s", "expected"], [
        ("aba: nisse#23", ("aba", "nisse", 23)),
        ("aba: nisse#23.5", ("aba", "nisse", 23, 5)),
        ("[foo]", ("foo",)),
        ("4-2", (4, 2))
    ]
)
def test__tokens(s, expected):
    assert expected == tokens(s)

def test__tokens_negative():
    assert tokens("4-2") == (4, 2)
    assert tokens("4-2", negative=True) == (4, -2)


def np_map(txt):
    return np.array(list(list(line.strip()) for line in txt.strip().split('\n')))
