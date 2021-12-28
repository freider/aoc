from collections import Counter

from lib.input import tokens, lines, aoc_input

src = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
src = aoc_input()

s = 0
q = 0
for line in lines(src):
    n, m, c, pw = tokens(line)
    if n <= Counter(pw)[c] <=m:
        s += 1
    if sum(c == x for x in [pw[n - 1], pw[m -1]]) == 1:
        q += 1


print(s, q)