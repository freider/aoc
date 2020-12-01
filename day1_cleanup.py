import itertools
from functools import reduce
from operator import mul

with open("inputs/1") as f:
	nums = [int(line.strip()) for line in f]


def solve(r=2):
	for tup in itertools.combinations(nums, r):
		if sum(tup) == 2020:
			print(reduce(mul, tup, 1))


def part1():
	solve(2)

def part2():
	solve(3)

part1()
part2()