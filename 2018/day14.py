from lib.input import aoc_input

num = int(aoc_input())
strnum = str(num)
starts = [3, 7]
s = starts.copy()
elf = [0, 1]

done = False
while len(s) < num + 10 or not done:
    added = [int(c) for c in str(s[elf[0]] + s[elf[1]])]
    s += added
    elf = [(e + s[e] + 1) % len(s) for e in elf]
    if strnum in ''.join(str(x) for x in s[len(s) - len(added) - len(strnum):]):
        done = True


print(''.join(str(x) for x in s[num:num+10]))
print(''.join(str(x) for x in s).index(strnum))
