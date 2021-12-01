from functools import lru_cache, cache

from lib.input import aoc_input
import regex


def part1():
    rules, msg = aoc_input().strip().split('\n\n')
    d = {}
    for l in rules.split('\n'):
        i, mpart = l.split(": ")
        d[i] = [case.split() for case in mpart.split(" | ")]

    def matches(i, s):
        if '"' in i:
            m = i.strip('"')
            if s.startswith(m):
                yield len(m)
            else:
                return
        else:
            v = d[i]
            for case in v:
                ps = [0]
                for part in case:
                    new_ps = []
                    for p in ps:
                        for m in matches(part, s[p:]):
                            new_ps.append(p + m)
                    ps = new_ps
                yield from iter(ps)

    ans = 0
    for line in msg.split("\n"):
        ans += any(x == len(line) for x in matches('0', line))
    print(ans)


def part2():
    rules, msg = aoc_input().strip().split('\n\n')
    d = {}
    for l in rules.split('\n'):
        i, mpart = l.split(": ")
        if i == "8":
            mpart = "42 | 42 8"
        elif i == "11":
            mpart = "42 31 | 42 11 31"
        d[i] = [case.split() for case in mpart.split(" | ")]

    def matches(i, s):
        if '"' in i:
            m = i.strip('"')
            if s.startswith(m):
                yield len(m)
            else:
                return
        else:
            v = d[i]
            for case in v:
                ps = [0]
                for part in case:
                    new_ps = []
                    for p in ps:
                        for m in matches(part, s[p:]):
                            new_ps.append(p + m)
                    ps = new_ps
                yield from iter(ps)

    ans = 0
    for line in msg.split("\n"):
        ans += any(x == len(line) for x in matches('0', line))
    print(ans)


def part2_re():
    rules, msg = aoc_input().strip().split('\n\n')
    d = {}
    for l in rules.split('\n'):
        i, mpart = l.split(": ")
        d[i] = [case.split() for case in mpart.split(" | ")]

    @cache
    def getre(i):
        if i == "8":
            return "{}+".format(getre("42"))
        elif i == "11":
            return "(?P<g11>{a}{b}|{a}(?&g11){b})".format(a=getre("42"), b=getre("31"))

        parts = []
        for ps in d[i]:
            if ps[0].startswith('"'):
                return ps[0].strip('"')
            else:
                parts.append(''.join(getre(j) for j in ps))

        joined = "|".join(parts)
        return f"({joined})"

    p = regex.compile(getre("0"))

    print(sum(1 for m in msg.split("\n") if p.fullmatch(m)))


if __name__ == "__main__":
    #part1()
    #part2()
    #part2_re()
    print(regex.match("((?R)a|a)", "aaaa"))