from lib.input import aoc_input, ints

print(sum(ints(aoc_input())))  # part 1

s = set()
c = 0
while True:
    for i in ints(aoc_input()):
        c += i
        if c in s:
            print(c)  # part 2
            exit()
        s.add(c)
