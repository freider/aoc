with open("inputs/1") as f:
	nums = [int(line.strip()) for line in f]


def part1():
	for i, n in enumerate(nums):
		for m in nums[i:]:
			if n + m == 2020:
				print(n * m)


def part2():
	for i, n in enumerate(nums):
		for j, m in enumerate(nums[i:]):
			for o in nums[i+j:]:
				if n + m + o == 2020:
					print(n * m * o)


if __name__ == "__main__":
	part1()
	part2()
