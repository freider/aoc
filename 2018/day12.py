from itertools import count

from lib.input import chunks, aoc_input, lines, pb_input

p1, p2 = chunks(aoc_input())
state = p1.split()[2]
d = {}
for l in lines(p2):
    inp, _, out = l.split()
    d[inp] = out

totpad = 0

for i in range(20):
    padded = "...." + state + "...."
    totpad += 2
    state = "".join(d.get(padded[ci:ci+5], ".") for ci in range(len(padded) - 4)).rstrip(".")
    slen = len(state)
    rem = slen - len(state.lstrip("."))
    totpad -= rem
    state = state[rem:]

print(sum(i for i, v in enumerate(state, -totpad) if v == "#"))

prevpad = totpad
prevstate = state
for gen in count(21):
    padded = "...." + state + "...."
    totpad += 2
    state = "".join(d.get(padded[ci:ci+5], ".") for ci in range(len(padded) - 4)).rstrip(".")
    slen = len(state)
    rem = slen - len(state.lstrip("."))
    totpad -= rem
    state = state[rem:]
    if state == prevstate:
        curscore = sum(i for i, v in enumerate(state, -totpad) if v == "#")
        print(curscore + state.count("#") * (50000000000 - gen) * -(totpad - prevpad))
        break

    prevpad = totpad
    prevstate = state

