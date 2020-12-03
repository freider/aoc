from collections import Counter


def read():
    with open("inputs/2") as f:
        for line in f:
            p1, pw = line.strip().split(":")
            q1, c = p1.split(" ")
            low, high = [int(x) for x in q1.split("-")]
            yield low, high, c, pw


def part1():
    print(sum(1 if low <= Counter(pw).get(c, 0) <= high else 0 for low, high, c, pw in read()))


def part2():
    def valid(low, high, c, pw):
        # indexing works without 1/0 indexing adjustment because there is a leading space in pw from parsing
        return Counter([pw[low], pw[high]]).get(c, 0) == 1

    print(sum(1 if valid(*t) else 0 for t in read()))

if __name__ == "__main__":
    part1()
    part2()
