from lib.input import aoc_input

# 7 ** l % 20201227 = 9033205

def part1():
    nums = [int(x) for x in aoc_input().strip().split('\n')]
    loop_sizes = []
    for n in nums:
        v = 1
        for loop_size in range(1, 100000000):
            v = v*7 % 20201227
            if v == n:
                loop_sizes.append(loop_size)
                break
        else:
            assert False
    print(pow(nums[0], loop_sizes[1], 20201227))
    print(pow(nums[1], loop_sizes[0], 20201227))


def part2():
    lines = aoc_input().strip().split('\n')



if __name__ == "__main__":
    part1()
    part2()
