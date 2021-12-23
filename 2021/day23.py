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

def part1():
    src = """#############
#...........#
###C#A#B#D###
  #B#A#D#C#  
  #########  """
#     src = """#############
# #.A.........#
# ###.#B#C#D###
#   #A#B#C#D#
#   #########  """

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
        rooms = n[2:4, 3:10:2]
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
                if rooms[room_index, 0] == '.' and rooms[room_index, 1] in ('.', c):
                    #  can move into its room, unless blocked
                    if hi < entrypoints[room_index]:
                        a, b = sorted([hi + 1, entrypoints[room_index]])
                    else:
                        a, b = sorted([hi - 1, entrypoints[room_index]])

                    if (hallway[a:b+1] == '.').all():
                        newhall = hallway.copy()
                        newhall[hi] = '.'
                        newrooms = rooms.copy()
                        if rooms[room_index, 1] == '.':
                            extra_step = 2
                            newrooms[room_index, 1] = c
                        else:
                            extra_step = 1
                            newrooms[room_index, 0] = c

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



def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
