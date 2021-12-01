from collections import Counter

from lib.input import aoc_input


def part1():
    groups = aoc_input().strip().split('\n\n')
    print(sum(len(set("".join(g.split()))) for g in groups))


def part2():
    groups = aoc_input().strip().split('\n\n')

    def e(g):
        return set.intersection(*[set(p) for p in g.split('\n')])

    print(sum(len(e(g)) for g in groups))


if __name__ == "__main__":
    part1()
    part2()
