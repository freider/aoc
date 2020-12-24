from collections import defaultdict

from lib.input import aoc_input

offsets = [
    ("nw", (-1, -1)),
    ("ne", (-1, 1)),
    ("w", (0, -2)),
    ("e", (0, 2)),
    ("se", (1, 1)),
    ("sw", (1, -1)),
]


def both():
    lines = aoc_input().strip().split('\n')
    flips = {}
    for l in lines:
        ref = (0, 0)
        while l:
            for prefix, offset in offsets:
                if l.startswith(prefix):
                    ref = (ref[0] + offset[0], ref[1] + offset[1])
                    l = l[len(prefix):]
        flips[ref] = not flips.get(ref, False)
    print(sum(1 for x in flips.values() if x))

    for day in range(100):
        adj = defaultdict(int)
        for pix, v in flips.items():
            if v:
                for _, o in offsets:
                    n = pix[0] + o[0], pix[1] + o[1]
                    adj[n] += 1
        newflips = {}

        for pix in set(flips.keys()) | set(adj.keys()):
            v = flips.get(pix, False)
            if v and (adj[pix] == 0 or adj[pix] > 2):
                newflips[pix] = False
            elif not v and (adj[pix] == 2):
                newflips[pix] = True
            else:
                newflips[pix] = v
        flips = newflips

    numblack = sum(1 for x in flips.values() if x)
    print(numblack)


if __name__ == "__main__":
    both()
