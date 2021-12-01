import re
from lib.input import aoc_input, pb_input


def data():
    yield from aoc_input().split('\n\n')


req = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
}


def passports():
    for p in data():
        parts = p.split()
        d = {}
        for x in parts:
            k, v = x.split(":")
            d[k] = v
        yield d


def isvalid(d):
    a = set(d.keys())
    if a & req != req:
        return False
    if not 1920 <= int(d["byr"]) <= 2002:
        return False
    if not 2010 <= int(d["iyr"]) <= 2020:
        return False
    if not 2020 <= int(d["eyr"]) <= 2030:
        return False
    m = re.match(r"([\d]+)(in|cm)", d["hgt"])
    if not m:
        return False
    if m.groups()[1] == "cm":
        if not 150 <= int(m.groups()[0]) <= 193:
            return False
    elif m.groups()[1] == "in":
        if not 59 <= int(m.groups()[0]) <= 76:
            return False
    else:
        return False

    if not re.match(r"#[0-9a-f]{6}", d["hcl"]):
        return False

    if d["ecl"] not in "amb blu brn gry grn hzl oth":
        return False

    if len(d["pid"]) != 9 or not d["pid"].isdigit():
        return False

    return True


def part1():
    def t():
        for d in passports():
            a = set(d.keys())
            if a & req == req:
                yield 1
    print(sum(t()))


def part2():
    def t():
        for d in passports():
            if isvalid(d):
                yield 1
    print(sum(t()))


if __name__ == "__main__":
    part1()
    part2()
