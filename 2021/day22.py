import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def pairs(seq):
    for i in range(len(seq) - 1):
        yield seq[i], seq[i + 1]


def part1():
    src = """"""
    src = aoc_input()

    ps = set()
    for line in lines(src):
        n = np.array(ints(line, negative=True))
        if ((n >= -50) & (n <= 50)).all():
            p1 = Point(n[0], n[2], n[4])
            p2 = Point(n[1], n[3], n[5])

            for p in Point.box_points(p1, p2):
                if line.startswith("on"):
                    ps.add(p)
                elif p in ps:
                    ps.remove(p)

    print(len(ps))


def part2():
    src = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
    src = aoc_input()

    cubes = []  # non overlapping positive cubes

    for it, line in enumerate(lines(src)):
        print(it, len(cubes))
        n = np.array(ints(line, negative=True))
        # if not ((n >= -50) & (n <= 50)).all():
        #     continue

        p1 = np.array([n[0], n[2], n[4]])
        p2 = np.array([n[1], n[3], n[5]]) + 1

        state = line.startswith("on")

        toremove = set()
        intersections = []

        # first remove all full overlaps
        for i, c in enumerate(cubes):
            o1, o2 = c
            if (p1 <= o1).all() and (p2 >= o2).all():
                # overlaps the entire old cube
                toremove.add(i)
            elif (p2 <= o1).any() or (p1 >= o2).any():
                # completely outside of the region
                pass
            else:
                # intersection
                intersections.append((o1, o2, True))
                toremove.add(i)

        intersections.append((p1, p2, state))
        print(f'{len(intersections)} intersection to process')

        def pointstate(p):
            for b1, b2, s in reversed(intersections):
                if (p >= b1).all() and (p < b2).all():
                    return s
            return False

        if toremove:
            print(f"removing {len(toremove)} old cubes")
            cubes = [c for i, c in enumerate(cubes) if i not in toremove]

        axi_vals = [set() for _ in range(3)]
        for p1, p2, _ in intersections:
            for i in range(3):
                axi_vals[i] |= {p1[i], p2[i]}

        sorted_vals = [
            sorted(v)
            for v in axi_vals
        ]

        added_cubes = 0
        for x1, x2 in pairs(sorted_vals[0]):
            for y1, y2 in pairs(sorted_vals[1]):
                for z1, z2 in pairs(sorted_vals[2]):
                    p1 = np.array([x1, y1, z1])
                    p2 = np.array([x2, y2, z2])
                    if pointstate(p1):
                        cubes.append((p1, p2))
                        added_cubes += 1
        print(f'adding {added_cubes}')

    print(f'{len(cubes)}')
    # for c in cubes:
    #     print(c)
    ans = 0
    for p1, p2 in cubes:
        ans += np.prod(p2 - p1)

    print('ans', ans)


def part2_slow_but_working():
    src = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

#     src = """on 3 6 3 6 3 6
# off 2 5 2 5 2 5
# on 1 3 1 3 1 3
# off 1 2 1 2 1 2"""
    # src = aoc_input()
    axi_vals = [set() for _ in range(3)]

    boxes = []

    for it, line in enumerate(lines(src)):
        n = np.array(ints(line, negative=True))
        if not ((n >= -50) & (n <= 50)).all():
            continue
        state = line.startswith("on")
        p1 = [n[0], n[2], n[4]]
        p2 = [n[1], n[3], n[5]]
        boxes.append((np.array(p1), np.array(p2), state))
        for i in range(3):
            axi_vals[i] |= {p1[i], p2[i]}

    sorted_vals = [
        sorted(v)
        for v in axi_vals
    ]
    for sv in sorted_vals:
        sv.append(sv[-1] + 1)

    def pointstate(p):
        for b1, b2, s in reversed(boxes):
            if (p >= b1).all() and (p <= b2).all():
                return s
        return False

    res = 0
    print([len(sorted_vals[i]) for i in range(3)])
    for it1, (x1, x2) in enumerate(pairs(sorted_vals[0])):
        print(it1)
        for y1, y2 in pairs(sorted_vals[1]):
            for z1, z2 in pairs(sorted_vals[2]):
                p1 = np.array([x1, y1, z1])
                p2 = np.array([x2, y2, z2])
                # add inner
                if ((p1 + 1) < p2).all():
                    #print("checking pointstate", p1 + 1, pointstate(p1 + 1))
                    if pointstate(p1 + 1):
                        #print('inner', np.prod(p2 - p1 - 1))
                        res += np.prod(p2 - p1 - 1)
                # 3 surfaces
                for i in range(3):
                    #  keep axis i constant
                    prod = 1
                    for j in range(3):
                        if i != j:
                            if p1[j] + 1 >= p2[j]:
                                break
                            prod *= p2[j] - p1[j] - 1
                    else:
                        surpoint = p1 + 1
                        surpoint[i] -= 1
                        if pointstate(surpoint):
                            #print("surface", prod)
                            res += prod

                # 3 edges
                for i in range(3):
                    #  keep axis i floating
                    if p1[i] + 1 < p2[i]:
                        edgelen = p2[i] - p1[i] - 1
                        surpoint = p1.copy()
                        surpoint[i] += 1
                        if pointstate(surpoint):
                            #print("edge", edgelen)
                            res += edgelen

                # 1 corners
                res += int(pointstate(np.array([x1, y1, z1])))

    print(res)
    #print(2758514936282235)

def part2_():
    src = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
    #src = aoc_input()

    cubes = []  # non overlapping

    for it, line in enumerate(lines(src)):
        print(it, len(cubes))
        n = np.array(ints(line, negative=True))
        p1 = Point(n[0], n[2], n[4])
        p2 = Point(n[1], n[3], n[5])
        state = line.startswith("on")

        toremove = []

        # first remove all full overlaps
        for c in cubes:
            o1, o2 = c
            if (p1.np() <= o1.np()).all() and (p2.np() >= o2.np()).all():
                # overlaps the entire old cube
                toremove.append(c)

        if toremove:
            print(f"removing {len(toremove)} full overlaps")
            for c in toremove:
                cubes.remove(c)

        toadd = []
        toremove = []
        for o1, o2 in cubes:
            if not ((o2.np() < p1.np()).any() or (o1.np() > p2.np()).any()):
                toremove.append((o1, o2))
                onpoints = [o1]
                offpoints = [o2]
                if state:
                    onpoints.append(p1)
                    offpoints.append(p2)
                else:
                    onpoints.append(p2)
                    offpoints.append(p1)

                xvals = []
                yvals = []
                zvals = []
                for q in onpoints:
                    x, y, z = q
                    xvals.append((x, 1))
                    yvals.append((y, 1))
                    zvals.append((z, 1))
                for q in offpoints:
                    x, y, z = q
                    xvals.append((x, -1))
                    yvals.append((y, -1))
                    zvals.append((z, -1))
                xvals.sort()
                yvals.sort()
                zvals.sort()

                x, xon = xvals[0]
                y, yon = yvals[0]
                z, zon = yvals[0]
                on = xon + yon + zon
                for nx, nxon in xvals[1:]:
                    for ny, nyon in yvals[1:]:
                        for nz, nzon in zvals[1:]:
                            if on > 0:
                                b1 = Point(x, y, z)
                                b2 = Point(nx, ny, nz)
                                toadd.append((b1, b2))
                            z = nz
                            on += nzon
                        y = ny
                        on += nyon
                    x = nx
                    on += nxon
        else:
            # no overlap with existing
            if state:
                toadd.append((p1, p2))
        for r in toremove:
            cubes.remove(r)
        print("adding", len(toadd))
        cubes += toadd


    on = 0
    for c in cubes:
        on += np.prod((p2 + Point(1, 1, 1) - p1).np())

    print(on)

if __name__ == "__main__":
    #part1()
    part2()
