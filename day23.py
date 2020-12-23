from dataclasses import dataclass
from itertools import chain

from lib.input import aoc_input, pb_input


class Node:
    next = None
    lower = None

    def __init__(self, label):
        self.label = label


def find(n, target):
    while n.label != target:
        n = n.next
    return n


def it(cups, max_l):
    cups = cups[1:] + cups[:1]  # shift current to end
    cur = cups[-1]
    picked = cups[:3]
    cups = cups[3:]
    dest_l = cur - 1
    while True:
        if dest_l in picked:
            dest_l -= 1
        elif dest_l < 1:
            dest_l = max_l
        else:
            break
    dest_i = cups.index(dest_l)
    newcups = cups[:dest_i+1] + picked + cups[dest_i+1:]
    return newcups


def part1():
    cups = [int(c) for c in aoc_input().strip()]
    print(cups)
    for i in range(100):
        cups = it(cups, 9)
    start_i = (cups.index(1) + 1) % len(cups)
    comb = cups[start_i:] + cups[:start_i-1]
    print(''.join(str(x) for x in comb))


def it_re(cur, lookup, max_l):
    removed = [cur.next, cur.next.next, cur.next.next.next]
    removed_v = [n.label for n in removed]
    cur.next = removed[-1].next
    dest_l = cur.label - 1
    while True:
        if dest_l in removed_v:
            dest_l -= 1
        elif dest_l < 1:
            dest_l = max_l
        else:
            break
    dest = lookup[dest_l]
    removed[-1].next = dest.next
    dest.next = removed[0]
    return cur.next


def part1_re():
    prev = None
    first = None
    lookup = {}
    for v in chain([int(c) for c in aoc_input().strip()]):
        new = Node(v)
        lookup[v] = new
        if not first:
            first = new
        if prev:
            prev.next = new

        prev = new

    prev.next = first

    cur = first
    for i in range(100):
        cur = it_re(cur, lookup, 9)

    start_i = lookup[1]
    ans = []
    c = start_i.next
    i = 0
    while c != start_i:
        ans.append(c.label)
        c = c.next
        i += 1

    print(''.join(str(x) for x in ans))


def part2():
    prev = None
    first = None
    lookup = {}
    for v in chain([int(c) for c in aoc_input().strip()], range(10, 1000001)):
        new = Node(v)
        lookup[v] = new
        if not first:
            first = new
        if prev:
            prev.next = new

        prev = new

    prev.next = first

    cur = first
    for i in range(10000000):
        if i%10000 == 0:
            print(i)
        cur = it_re(cur, lookup, 1000000)

    start_i = lookup[1]
    ans = []
    c = start_i.next
    i = 0
    while c != start_i:
        ans.append(c.label)
        c = c.next
        i += 1

    print(lookup[1].next.label * lookup[1].next.next.label)


if __name__ == "__main__":
   part1()
   part1_re()
   part2()
