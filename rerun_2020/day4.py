import re

from lib.input import chunks, tokens, aoc_input

src = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

src = aoc_input()
req = set("byr iyr eyr hgt hcl ecl pid".split())

s = 0
t = 0
for c in chunks(src):
    entries = c.split()
    ls = dict(e.split(":") for e in entries)

    if (req - set(ls.keys())):
        continue

    s += 1

    if not (1920 <= int(ls["byr"]) <= 2002):
        continue

    if not (2010 <= int(ls["iyr"]) <= 2020):
        continue

    if not (2020 <= int(ls["eyr"]) <= 2030):
        continue

    if ls["hgt"].endswith("cm"):
        if not (150 <= int(ls["hgt"][:-2]) <= 193):
            continue
    elif ls["hgt"].endswith("in"):
        if not (59 <= int(ls["hgt"][:-2]) <= 76):
            continue
    else:
        continue

    if not re.fullmatch("#[a-f0-9]{6}$", ls["hcl"]):
        continue

    if not ls["ecl"] in ("amb blu brn gry grn hzl oth".split()):
        continue

    if not re.fullmatch("\d{9}", ls["pid"]):
        continue

    t += 1


print(s)
print(t)