import sys
import re
from collections import Counter, defaultdict
import heapq
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def totup(state):
    return (
        tuple(state[0]),
        tuple(tuple(row) for row in state[1])
    )

def tonp(state):
    return (
        np.array(list(state[0])),
        np.array(list(list(row) for row in state[1]))
    )

movecosts = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}
entrypoints = [2, 4, 6, 8]

def est(state):
    hallway, rooms = state
    tot = 0
    for i, room in enumerate(rooms):
        current_x = entrypoints[i]

        for depth, c in enumerate(room):
            if c != '.':
                target_x = entrypoints[ord(c) - ord('A')]
                if target_x != current_x:
                    tot += movecosts[c] * (abs(target_x - current_x) + depth + 2)
    for x, c in enumerate(hallway):
        if c != '.':
            target_x = entrypoints[ord(c) - ord('A')]
            tot += movecosts[c] * (abs(target_x - x) + 1)

    return tot


def part1():
    src = """#############
#...........#
###C#A#B#D###
  #D#C#B#A#  
  #D#B#A#C#  
  #B#A#D#C#  
  #########  """
    m = np_map(src, strip=False)

    def state(n):
        hallway = n[1][1:-1]
        rooms = n[2:-1, 3:10:2]
        return hallway, rooms.T

    print(state(m))

    target = state(np_map("""#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #A#B#C#D#  
  #A#B#C#D#  
  #########  """, strip=False))

    print(est(target))
    q = [
        (0, totup(state(m)))
    ]
    best = {}
    best[totup(state(m))] = 0
    vis = set()
    while q:
        costest, state = heapq.heappop(q)
        if state in vis:
            continue
        vis.add(state)
        cost = best[state]
        (hallway, rooms) = tonp(state)
        #print('visiting', hallway, rooms)

        if (rooms == target[1]).all():
            print("Cost:", cost)
            return

        could_enter_room = False
        for hi, c in enumerate(hallway):
            if c != '.':
                room_index = ord(c) - ord('A')
                if rooms[room_index, 0] == '.' and ((rooms[room_index, 1:] == '.') | (rooms[room_index, 1:] == c)).all():
                    #  can move into its room, unless blocked
                    if hi < entrypoints[room_index]:
                        a, b = sorted([hi + 1, entrypoints[room_index]])
                    else:
                        a, b = sorted([hi - 1, entrypoints[room_index]])

                    if (hallway[a:b+1] == '.').all():
                        newhall = hallway.copy()
                        newhall[hi] = '.'
                        newrooms = rooms.copy()
                        extra_step = 0
                        for i, rc in enumerate(rooms[room_index]):
                            if rc == '.':
                                extra_step += 1
                            else:
                                break
                        newrooms[room_index, extra_step - 1] = c

                        newcost = cost + (b+1-a + extra_step) * movecosts[c]
                        newstate = totup((newhall, newrooms))
                        if newstate not in best or newcost < best[newstate]:
                            best[newstate] = newcost
                            heapq.heappush(q, (newcost + est(newstate), newstate))
                        could_enter_room = True

        if not could_enter_room:
            for room_i, room in enumerate(rooms):
                for depth, c in enumerate(room):
                    currx = entrypoints[room_i]
                    if c != '.':
                        #  move out into all possible hallway locations
                        for mx in range(len(hallway)):
                            if mx in entrypoints:
                                continue
                            badx = False
                            for room_i2, room2 in enumerate(rooms):
                                for depth2, c2 in enumerate(room2):
                                    if room_i2 == room_i and depth == depth2:
                                        continue
                                    if c2 != '.':
                                        curx2 = entrypoints[room_i2]
                                        destx = entrypoints[ord(c2) - ord('A')]
                                        a, b = sorted([curx2, destx])
                                        if a < mx < b:
                                            badx = True
                                            break
                                if badx:
                                    break
                            if badx:
                                continue

                            a, b = sorted([currx, mx])
                            if (hallway[a:b+1] == '.').all():
                                # can move to mx
                                newhall = hallway.copy()
                                newrooms = rooms.copy()
                                newhall[mx] = c
                                newrooms[room_i, depth] = '.'
                                newcost = cost + (b+1-a + depth) * movecosts[c]
                                newstate = totup((newhall, newrooms))
                                if newstate not in best or newcost < best[newstate]:
                                    best[newstate] = newcost
                                    heapq.heappush(q, (newcost + est(newstate), newstate))
                        break  # only move first guy



def part2():
    src = """#############
#...........#
###C#A#B#D###
  #B#A#D#C#  
  #########  """

    #src = aoc_input()
    m = np_map(src, strip=False)
    movecosts = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    def state(n):
        hallway = n[1][1:-1]
        rooms = n[2:-1, 3:10:2]
        return hallway, rooms.T

    print(state(m))
    entrypoints = [2, 4, 6, 8]
    target = state(np_map("""#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #########  """, strip=False))

    q = [
        (0, totup(state(m)))
    ]
    best = {}
    best[totup(state(m))] = 0

    while q:
        cost, state = heapq.heappop(q)
        (hallway, rooms) = tonp(state)
        #print('visiting', hallway, rooms)

        if (rooms == target[1]).all():
            print("Cost:", cost)
            return

        could_enter_room = False
        for hi, c in enumerate(hallway):
            if c != '.':
                room_index = ord(c) - ord('A')
                if rooms[room_index, 0] == '.' and ((rooms[room_index, 1:] == '.') | (rooms[room_index, 1:] == c)).all():
                    #  can move into its room, unless blocked
                    if hi < entrypoints[room_index]:
                        a, b = sorted([hi + 1, entrypoints[room_index]])
                    else:
                        a, b = sorted([hi - 1, entrypoints[room_index]])

                    if (hallway[a:b+1] == '.').all():
                        newhall = hallway.copy()
                        newhall[hi] = '.'
                        newrooms = rooms.copy()
                        extra_step = 0
                        for i, rc in enumerate(rooms[room_index]):
                            if rc == '.':
                                extra_step += 1
                            else:
                                break
                        newrooms[room_index, i - 1] = c
                        newcost = cost + (b+1-a + extra_step) * movecosts[c]
                        newstate = totup((newhall, newrooms))
                        if newstate not in best or newcost < best[newstate]:
                            best[newstate] = newcost
                            heapq.heappush(q, (newcost, newstate))
                        could_enter_room = True

        if not could_enter_room:
            for room_i, room in enumerate(rooms):
                for depth, c in enumerate(room):
                    currx = entrypoints[room_i]
                    if c != '.':
                        #  move out into all possible hallway locations
                        for mx in range(len(hallway)):
                            if mx in entrypoints:
                                continue

                            a, b = sorted([currx, mx])
                            if (hallway[a:b+1] == '.').all():
                                # can move to mx
                                newhall = hallway.copy()
                                newrooms = rooms.copy()
                                newhall[mx] = c
                                newrooms[room_i, depth] = '.'
                                newcost = cost + (b+1-a + depth) * movecosts[c]
                                newstate = totup((newhall, newrooms))
                                if newstate not in best or newcost < best[newstate]:
                                    best[newstate] = newcost
                                    heapq.heappush(q, (newcost, newstate))
                        break  # only move first guy


if __name__ == "__main__":
    part1()
    #part2()
