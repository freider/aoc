import itertools
from functools import reduce
from operator import mul

with open("inputs/1") as f:
	nums = [int(line.strip()) for line in f]


def solve(nums, tupsize):
	for tup in itertools.combinations(nums, tupsize):
		if sum(tup) == 2020:
			print(reduce(mul, tup, 1))


def part1():
	solve(nums, 2)


def part2():
	solve(nums, 3)


if __name__ == "__main__":
	part1()
	part2()
