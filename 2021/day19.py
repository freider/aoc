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


def rot(p, rdef):
    ix, flipix = rdef
    v = [p.np()[i] * flipix[j] for j, i in enumerate(ix)]
    return Point(*v)

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
        for i, line in enumerate(ls[1:]):
            pos = ints(line, negative=True)
            inpoints.append(Point(*pos))
        inchunks.append(inpoints)

    def allrots(ps):
        for ix in permutations([0, 1, 2]):
            for flipmask in range(8):
                flipix = [-1 if c == "1" else 1 for c in f'{flipmask:3b}']
                rotpoints = []
                for p in ps:
                    rotpoints.append(rot(p, [ix, flipix]))
                yield set(rotpoints), [ix, flipix]

    chunkmatches = []
    for chunkid1, ps1 in enumerate(inchunks):
        for _chunkid2, ps2 in enumerate(inchunks[chunkid1 + 1:]):
            chunkid2 = chunkid1 + 1 + _chunkid2
            for ps2rot, rotdef in allrots(ps2):
                diffs_to_points = Counter(p1 - p2 for p1 in ps1 for p2 in ps2rot)
                for trans, n in diffs_to_points.items():
                    if n >= 12:
                        print('match', (chunkid1, chunkid2))
                        chunkmatches.append((chunkid1, chunkid2))
                        break
                else:
                    continue
                break
    print(chunkmatches)  # intermediate cache of the heaviest lifting

    rotdefs = defaultdict(list)

    for _chunkid1, _chunkid2 in chunkmatches:
        for chunkid1, chunkid2 in [(_chunkid1, _chunkid2), (_chunkid2, _chunkid1)]:
            ps1 = inchunks[chunkid1]
            ps2 = inchunks[chunkid2]
            for ps2rot, rotdef in allrots(ps2):
                diffs_to_points = Counter(p1 - p2 for p1 in ps1 for p2 in ps2rot)
                for trans, n in diffs_to_points.items():
                    if n >= 12:
                        rotdefs[chunkid2].append((chunkid1, rotdef, trans))
                        break
                else:
                    continue
                break

    pprint(rotdefs)  # cache heavy intermediate result

    points = set()
    for cid, ic in enumerate(inchunks):
        for p in ic:
            points.add((cid, p))

    while 1:
        didadd = False
        for cid, p in points.copy():
            for nextcid, rotdef, trans in rotdefs[cid]:
                new = rot(p, rotdef) + trans
                if (nextcid, new) not in points:
                    points.add((nextcid, new))
                    didadd = True
        if didadd:
            continue
        break

    ps = set(p for cid, p in points if cid == 0)
    print(len(ps))


def part2():
    rotdefs = {0: [(1, [(2, 0, 1), [-1, 1, -1]], Point(105, -29, 1057)),
                   (5, [(2, 1, 0), [1, 1, -1]], Point(1153, 127, 86)),
                   (15, [(2, 1, 0), [-1, 1, 1]], Point(1292, 81, -88)),
                   (22, [(0, 1, 2), [-1, 1, -1]], Point(18, 1198, 75))],
               1: [(0, [(1, 2, 0), [1, -1, -1]], Point(29, 1057, 105)),
                   (6, [(2, 1, 0), [1, -1, 1]], Point(63, -1114, -58)),
                   (16, [(0, 1, 2), [-1, 1, -1]], Point(-52, -89, -1213)),
                   (21, [(2, 0, 1), [-1, 1, -1]], Point(-148, -2, 1296)),
                   (27, [(2, 1, 0), [-1, -1, -1]], Point(-77, 49, -1085))],
               2: [(11, [(2, 1, 0), [-1, -1, -1]], Point(-36, 1307, -55)),
                   (15, [(0, 2, 1), [-1, -1, -1]], Point(-85, -54, -1228)),
                   (25, [(1, 2, 0), [1, 1, 1]], Point(-12, -1202, 84))],
               3: [(19, [(2, 0, 1), [1, -1, -1]], Point(39, 4, 1284))],
               4: [(29, [(2, 1, 0), [-1, 1, 1]], Point(77, -176, 1218)),
                   (32, [(1, 0, 2), [-1, -1, -1]], Point(15, 42, 1158))],
               5: [(0, [(2, 1, 0), [-1, 1, 1]], Point(86, -127, -1153)),
                   (19, [(2, 1, 0), [-1, -1, -1]], Point(72, 14, -1106))],
               6: [(1, [(2, 1, 0), [1, -1, 1]], Point(58, -1114, -63)),
                   (18, [(0, 1, 2), [1, -1, -1]], Point(1270, 32, -86))],
               7: [(9, [(2, 1, 0), [-1, -1, -1]], Point(-49, -104, -1115)),
                   (16, [(1, 0, 2), [1, -1, 1]], Point(-1176, -73, 10))],
               8: [(32, [(0, 2, 1), [-1, -1, -1]], Point(1056, 67, -51))],
               9: [(7, [(2, 1, 0), [-1, -1, -1]], Point(-1115, -104, -49))],
               10: [(12, [(0, 1, 2), [1, -1, -1]], Point(-160, 1244, -63)),
                    (20, [(1, 2, 0), [1, 1, 1]], Point(51, -18, 1119)),
                    (24, [(2, 1, 0), [-1, 1, 1]], Point(-81, 1148, -158))],
               11: [(2, [(2, 1, 0), [-1, -1, -1]], Point(-55, 1307, -36))],
               12: [(10, [(0, 1, 2), [1, -1, -1]], Point(160, 1244, -63)),
                    (17, [(1, 0, 2), [1, -1, 1]], Point(-153, -132, 1309)),
                    (23, [(2, 0, 1), [1, -1, -1]], Point(62, -18, -1056))],
               13: [(14, [(1, 2, 0), [1, 1, 1]], Point(85, 85, 1245)),
                    (28, [(1, 2, 0), [-1, -1, 1]], Point(1156, 4, 22))],
               14: [(13, [(2, 0, 1), [1, 1, 1]], Point(-1245, -85, -85)),
                    (23, [(0, 2, 1), [-1, 1, 1]], Point(13, 1191, 45))],
               15: [(0, [(2, 1, 0), [1, 1, -1]], Point(88, -81, 1292)),
                    (2, [(0, 2, 1), [-1, -1, -1]], Point(-85, -1228, -54)),
                    (27, [(1, 2, 0), [1, -1, -1]], Point(-1215, -10, 102)),
                    (31, [(1, 2, 0), [1, 1, 1]], Point(-87, -1103, 27))],
               16: [(1, [(0, 1, 2), [-1, 1, -1]], Point(-52, 89, -1213)),
                    (7, [(1, 0, 2), [-1, 1, 1]], Point(-73, 1176, -10)),
                    (18, [(2, 1, 0), [-1, 1, 1]], Point(120, 1235, 24))],
               17: [(12, [(1, 0, 2), [-1, 1, 1]], Point(-132, 153, -1309)),
                    (30, [(1, 2, 0), [-1, -1, 1]], Point(-21, -1176, 123))],
               18: [(6, [(0, 1, 2), [1, -1, -1]], Point(-1270, 32, -86)),
                    (16, [(2, 1, 0), [1, 1, -1]], Point(-24, -1235, 120))],
               19: [(3, [(1, 2, 0), [-1, -1, 1]], Point(4, 1284, -39)),
                    (5, [(2, 1, 0), [-1, -1, -1]], Point(-1106, 14, 72))],
               20: [(10, [(2, 0, 1), [1, 1, 1]], Point(-1119, -51, 18))],
               21: [(1, [(1, 2, 0), [1, -1, -1]], Point(2, 1296, -148)),
                    (32, [(1, 2, 0), [-1, -1, 1]], Point(-1257, 176, 34))],
               22: [(0, [(0, 1, 2), [-1, 1, -1]], Point(18, -1198, 75)),
                    (23, [(1, 0, 2), [1, 1, -1]], Point(1294, 93, 63))],
               23: [(12, [(1, 2, 0), [-1, -1, 1]], Point(-18, -1056, -62)),
                    (14, [(0, 2, 1), [-1, 1, 1]], Point(13, -45, -1191)),
                    (22, [(1, 0, 2), [1, 1, -1]], Point(-93, -1294, 63)),
                    (26, [(2, 0, 1), [-1, 1, -1]], Point(1216, -76, 2))],
               24: [(10, [(2, 1, 0), [1, 1, -1]], Point(158, -1148, -81))],
               25: [(2, [(2, 0, 1), [1, 1, 1]], Point(-84, 12, 1202))],
               26: [(23, [(1, 2, 0), [1, -1, -1]], Point(76, 2, 1216))],
               27: [(1, [(2, 1, 0), [-1, -1, -1]], Point(-1085, 49, -77)),
                    (15, [(2, 0, 1), [-1, 1, -1]], Point(102, 1215, -10)),
                    (32, [(2, 1, 0), [1, -1, 1]], Point(-170, -1071, -37))],
               28: [(13, [(2, 0, 1), [1, -1, -1]], Point(-22, 1156, 4))],
               29: [(4, [(2, 1, 0), [1, 1, -1]], Point(-1218, 176, 77))],
               30: [(17, [(2, 0, 1), [1, -1, -1]], Point(-123, -21, -1176))],
               31: [(15, [(2, 0, 1), [1, 1, 1]], Point(-27, 87, 1103)),
                    (32, [(2, 1, 0), [-1, 1, 1]], Point(-41, 42, -1165))],
               32: [(4, [(1, 0, 2), [-1, -1, -1]], Point(42, 15, 1158)),
                    (8, [(0, 2, 1), [-1, -1, -1]], Point(1056, -51, 67)),
                    (21, [(2, 0, 1), [1, -1, -1]], Point(-34, -1257, 176)),
                    (27, [(2, 1, 0), [1, -1, 1]], Point(37, -1071, 170)),
                    (31, [(2, 1, 0), [1, 1, -1]], Point(1165, -42, -41))]}

    points = set()
    for i in range(len(rotdefs)):
        points.add((i, Point(0, 0, 0)))

    while 1:
        didadd = False
        for cid, p in points.copy():
            for nextcid, rotdef, trans in rotdefs[cid]:
                new = rot(p, rotdef) + trans
                if (nextcid, new) not in points:
                    points.add((nextcid, new))
                    didadd = True
        if didadd:
            continue
        break

    ps = set(p for cid, p in points if cid == 0)
    maxman = 0
    for p1 in ps:
        for p2 in ps:
            maxman = max(maxman, np.abs((p2 - p1).np()).sum())
    print(maxman)


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