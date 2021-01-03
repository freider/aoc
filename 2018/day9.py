from lib.input import aoc_input, ints

players, max_m = ints(aoc_input())
player_score = [0] * players
max_m *= 100

def ccw(ix, n):
    if n == 0:
        return ix
    return ccw(circ[ix][0], n-1)


def cw(ix, n):
    if n == 0:
        return ix
    return cw(circ[ix][1], n-1)


circ = [[0, 0]] + [None] * max_m
current = 0
player_ix = 0
for m in range(1, max_m + 1):
    if m % 23 == 0:
        rem = ccw(current, 7)
        pre, aft = circ[rem]
        circ[pre][1] = aft
        circ[aft][0] = pre
        player_score[player_ix] += m + rem
        current = aft
    else:
        pre = cw(current, 1)
        aft = cw(current, 2)
        circ[m] = [pre, aft]
        circ[aft][0] = m
        circ[pre][1] = m
        current = m

    player_ix = (player_ix + 1) % players

# too low: 304084
print(max(player_score))
