from lib.input import aoc_input

src = aoc_input()
m = 0

al = set()

for t in src.split():
    a = int(t[:-3].replace("F", "0").replace("B", "1"), 2)
    b = int(t[-3:].replace("L", "0").replace("R", "1"), 2)

    al.add(a * 8 + b)

print(max(al))

for i in range(min(al), max(al) + 1):
    if i not in al:
        print(i)
        break
