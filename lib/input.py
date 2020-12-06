import os
import re
import subprocess
from typing import Union
import numpy as np
import sys

from lib.aoc_api import Aoc


def infer_day():
    return re.search(r'day([\d]+)', sys.argv[0]).group(1)


def pb_input():
    return subprocess.check_output('pbpaste', encoding='utf8')


def aoc_input(fn: Union[str, int, None] = None):
    if fn is None:
        fn = infer_day()

    relpath = f"inputs/{fn}"
    if os.path.exists(relpath):
        with open(relpath) as f:
            return f.read()
    else:
        if not str(fn).isdigit():
            raise Exception("Can only fetch full day input")
        txt = Aoc().fetch_input_for_day(fn).strip()
        with open(relpath, 'w') as f:
            f.write(txt)
        return txt


def np_map(txt):
    return np.array(list(list(line.strip()) for line in txt.strip().split('\n')))
