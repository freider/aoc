from collections import deque
from dataclasses import dataclass

from itertools import count

from lib.input import aoc_input, lines
from lib.point import Point

obst = set()
unit = []


@dataclass
class Unit:
    type: str
    pos: Point
    hp: int = 200
    ap: int = 3

    def __hash__(self):
        return hash(self.pos)


# inp = lines(aoc_input("15ex"))
inp = lines(aoc_input())

for y, row in enumerate(inp):
    for x, c in enumerate(row):
        p = Point(y, x)
        if c == "#":
            obst.add(p)
        if c in "EG":
            unit.append(Unit(c, p))


diffs = [
    Point(-1, 0),
    Point(0, -1),
    Point(0, 1),
    Point(1, 0)
]


def step(a):
    goals = set()
    upos = {u.pos: u for u in unit if u != a}
    for u in sorted(unit, key=lambda u: u.pos):
        if a.type != u.type:
            for d in diffs:
                c = u.pos + d
                if c in obst or c in upos:
                    continue
                goals.add(c)

    parent = {a.pos: None}
    q = deque([a.pos])
    found = a.pos if a.pos in goals else None
    while q and not found:
        cur = q.popleft()
        for d in diffs:
            nxt = cur + d
            if nxt in parent or nxt in obst or nxt in upos:
                continue
            parent[nxt] = cur
            if nxt in goals:
                found = nxt
                break
            q.append(nxt)

    if found:
        cur = found
        path = []
        while cur:
            path.append(cur)
            cur = parent[cur]

        assert path[-1] == a.pos
        if len(path) > 1:
            move_target = path[-2]
            #print(f"moving {a} to {move_target}")
            a.pos = move_target

        adj = set()
        for u in sorted(unit, key=lambda u: u.pos):
            if a.type != u.type:
                for d in diffs:
                    c = u.pos + d
                    if c == a.pos:
                        adj.add(u)
        if adj:
            target = min(adj, key=lambda u: (u.hp, u.pos))
            target.hp -= a.ap
            if target.hp <= 0:
                #print(f"{target} dies")
                unit.remove(target)
        return True

    return False


def disp():
    upos = {u.pos: u for u in unit}
    for y in range(len(inp)):
        row = []
        for x in range(len(inp[0])):
            p = Point(y, x)
            if p in obst:
                row.append("#")
            elif p in upos:
                row.append(upos[p].type)
            else:
                row.append('.')
        print(''.join(row))

#disp()

for full_rounds in count(0):
    action = False
    for u in sorted(unit, key=lambda u: u.pos):
        if u.hp < 0:
            continue
        s = step(u)
        action = action or s

    if not action:
        print((full_rounds - 1) * sum(u.hp for u in unit))
        break

    print("rounds:", full_rounds)
    #disp()
#disp()

