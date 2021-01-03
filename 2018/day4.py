from collections import defaultdict, Counter
from datetime import datetime, timedelta

from lib.input import aoc_input, tokens, pb_input

guard = None
state = None
last_time = None
guardsleep = defaultdict(set)

inp = sorted(tokens(line) for line in aoc_input().split('\n'))

for toks in inp:
    time = datetime(toks[0], toks[1], toks[2], toks[3], toks[4])

    if last_time:
        while last_time != time:
            if last_time.hour == 0 and state == 'sleep':
                guardsleep[guard].add(last_time)
            last_time += timedelta(minutes=1)

    if toks[-1] == "shift":
        guard = toks[6]
        state = 'up'
    elif toks[-1] == "asleep":
        state = 'sleep'
    elif toks[-1] == "up":
        state = 'up'
    last_time = time


mostg = max(guardsleep.keys(), key=lambda g: len(guardsleep[g]))
c = Counter(t.minute for t in guardsleep[mostg])
mostmin = max(c.keys(), key=lambda t: c[t])
print(mostmin * mostg)

def f():
    for g, v in guardsleep.items():
        c = Counter(t.minute for t in v)
        g_mostmin = max(c.items(), key=lambda t: t[1])
        yield g, g_mostmin

g = max(f(), key=lambda x: x[1][1])
print(g)
print(g[0] * g[1][0])