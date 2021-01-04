from dataclasses import dataclass

from lib.input import aoc_input, lines, pb_input
from lib.point import Point

track = [list(l) for l in lines(aoc_input())]
shape = {
    '^': '|',
    'v': '|',
    '<': '-',
    '>': '-',
}
dir = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}
@dataclass
class Car:
    pos: Point
    v: Point
    state: int

    def vis(self):
        return {Point(*v): k for k, v in dir.items()}[self.v]


cars = []
for y, row in enumerate(track):
    for x, c in enumerate(row):
        if c in shape:
            row[x] = shape[c]
            cars.append(Car(Point(y, x), Point(*dir[c]), 0))


def disp():
    card = {c.pos: c.vis() for c in cars}
    for y, row in enumerate(track):
        print(''.join(c if not Point(y,x) in card else card[Point(y, x)] for x, c in enumerate(row)))

def tick(c):
    c.pos += c.v
    try:
        road = track[c.pos[0]][c.pos[1]]
    except:
        c.pos -= c.v
        track[c.pos[0]][c.pos[1]] = "#"
        disp()
        raise

    if road == "+":
        if c.state == 0:
            c.v = c.v.rot90(1)
        elif c.state == 2:
            c.v = c.v.rot90(3)
        c.state = (c.state + 1) % 3
    elif road == "/":
        if c.v[0]:
            c.v = c.v.rot90(3)
        else:
            c.v = c.v.rot90(1)
    elif road == "\\":
        if c.v[0]:
            c.v = c.v.rot90(1)
        else:
            c.v = c.v.rot90(3)


def f():
    while len(cars) > 1:
        cars.sort(key=lambda c: tuple(c.pos.np()))
        crashed = set()
        for i, c in enumerate(cars):
            if i not in crashed:
                tick(c)
                for i2, c2 in enumerate(cars):
                    if i2 not in crashed and i2 != i:
                        if c.pos == c2.pos:
                            crashed |= {i, i2}
                if len(cars) - len(crashed) == 1:
                    break

        for ci in sorted(crashed, reverse=True):
            yield ",".join(str(x) for x in cars[ci].pos.np()[::-1])
            del cars[ci]

crashes = f()
print(next(crashes))
for _ in crashes:
    pass
print(",".join(str(x) for x in cars[0].pos.np()[::-1]))
