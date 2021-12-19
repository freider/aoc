import sys
import re
from collections import Counter, defaultdict
from itertools import permutations
from pprint import pprint

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

    #src = aoc_input()
    inchunks = []

    for c in chunks(src):
        inpoints = []
        ls = lines(c)
        scanner = ints(ls[0])[0]
        for i, line in enumerate(ls[1:]):
            pos = ints(line, negative=True)
            inpoints.append((Point(*pos), (scanner, i)))
        inchunks.append(inpoints)

    def allrots(ps):
        for ix in permutations([0, 1, 2]):
            for flipix in [None, 0, 1, 2]:
                rotpoints = []
                for p, idx in ps:
                    v = [p.np()[i] * (-1 if j == flipix else 1) for j, i in enumerate(ix)]
                    rotpoints.append((Point(*v), idx))
                norm = min(rotpoints)[0]
                yield {p - norm: idx for p, idx in rotpoints}, [ix, flipix, norm]

    def rot(p, rdef):
        ix, flipix, norm = rdef
        v = [p.np()[i] * (-1 if j == flipix else 1) for j, i in enumerate(ix)]
        return Point(*v) - norm

    def unrot(p, rdef):
        ix, flipix, norm = rdef
        out = [None] * 3
        unnorm = (p + norm).np()
        for i in range(3):
            out[ix[i]] = unnorm[i] * (-1 if i == flipix else 1)
        return Point(*out)

    rotdefs = defaultdict(list)
    points = set()

    for i1, ps1 in enumerate(inchunks):
        for p, _ in ps1:
            points.add((i1, p))

        for i2, ps2 in enumerate(inchunks[i1 + 1:]):
            chunkid2 = i1 + 1 + i2
            for r1, rotdef in allrots(ps1):
                for r2, rotdef2 in allrots(ps2):
                    overlap = set(r1.keys()) & set(r2.keys())
                    if len(overlap) >= 12:
                        print(i1, chunkid2, 'overlap', len(overlap))
                        rotdefs[chunkid2].append((i1, rotdef, rotdef2))
                        rotdefs[i1].append((chunkid2, rotdef2, rotdef))
                        break
                else:
                    continue
                break

    pprint(rotdefs)
    while 1:
        didadd = False
        for cid, p in points.copy():
            for nextcid, r1, r2 in rotdefs[cid]:
                new = unrot(rot(p, r2), r1)
                if (nextcid, new) not in points:
                    points.add((nextcid, new))
                    didadd = True
        if didadd:
            continue
        break

    print(len(set(p for cid, p in points if cid == 0)))
    print("done")
    # WA: 67


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()

#
# def allrots(ps):
#     for ix in permutations([0, 1, 2]):
#         for flipmask in range(8):
#             flipmask = bin(flipmask)[2:]
#             flipmask = "0" * (3 - len(flipmask)) + flipmask
#             flipix = [-1 if c == "1" else 1 for c in flipmask]
#             rotpoints = []
#             for p, idx in ps:
#                 v = [p.np()[i] * flipix[j] for j, i in enumerate(ix)]
#                 rotpoints.append((Point(*v), idx))
#             minp = min(rotpoints)[0]
#             yield {p - minp: idx for p, idx in rotpoints}, (ix, flipix)