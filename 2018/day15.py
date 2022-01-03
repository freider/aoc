from collections import deque
from copy import deepcopy
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


#inp = lines(aoc_input("15ex"))
inp = lines(aoc_input())

for y, row in enumerate(inp):
    for x, c in enumerate(row):
        p = Point(y, x)
        if c == "#":
            obst.add(p)
        if c in "EG":
            unit.append(Unit(c, p))


class ElfException(Exception):
    pass

diffs = [
    Point(-1, 0),
    Point(0, -1),
    Point(0, 1),
    Point(1, 0)
]

def find(units, starts, target):
    parent = {s: None for s in starts}
    q = deque(starts)
    upos = {u.pos for u in units} - {target}
    found = target if target in starts else None

    while q and not found:
        cur = q.popleft()
        for d in diffs:
            nxt = cur + d
            if nxt in parent or nxt in obst or nxt in upos:
                continue
            parent[nxt] = cur
            if nxt == target:
                found = nxt
                break
            q.append(nxt)

    if found:
        cur = found
        path = []
        while cur:
            path.append(cur)
            cur = parent[cur]
        return path
    return []


def sim(unit, raise_on_elf=False):
    def step(a):
        points_in_range = []
        upos = {u.pos: u for u in unit if u != a}
        targets = sorted((u for u in unit if a.type != u.type and u.hp > 0), key=lambda u: u.pos)
        for u in targets:
            for d in diffs:
                c = u.pos + d
                if c in obst or c in upos or c in points_in_range:
                    continue
                points_in_range.append(c)
        
        if not(points_in_range):
            return len(targets) > 0

        if a.pos not in points_in_range:
            path = find(unit, points_in_range, a.pos)
        
            if path: # there is a reachable target
                assert path[0] == a.pos
                # find best route to target
                path = find(unit, [a.pos], path[-1])

                if len(path) > 1:
                    # move if we are not at target
                    move_target = path[-2]
                    a.pos = move_target

        adj = set()
        for u in targets:
            for d in diffs:
                c = u.pos + d
                if c == a.pos:
                    adj.add(u)
        if adj:
            target = min(adj, key=lambda u: (u.hp, u.pos))
            target.hp -= a.ap
            if target.hp <= 0:
                if target.type == "E" and raise_on_elf:
                    raise ElfException()
                else:
                    unit.remove(target)
    
        return len(targets) > 0

    full_rounds = 0
    while True:
        for u in sorted(unit, key=lambda u: u.pos):
            if u.hp <= 0:
                continue
            if not step(u):
                break
        else:
            full_rounds += 1
            continue

        return full_rounds, sum(u.hp for u in unit), (full_rounds) * sum(u.hp for u in unit)



def disp(unit):
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


#part1
print(sim(deepcopy(unit)))

def ok(ap):
    test_unit = deepcopy(unit)
    for u in test_unit:
        if u.type == "E":
            u.ap = ap
    try:
        return sim(test_unit, raise_on_elf=True)
    except ElfException:
        return False


# hi = 4
#
# while True:
#     print(hi)
#     if ok(hi):
#        break
#     hi *= 2

for i in count(4):
    print(i)
    stat = ok(i)
    if stat:
        print(stat)
        break

# too low : 50912
# too high: 52096