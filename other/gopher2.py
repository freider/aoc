import heapq
from copy import deepcopy

import sys


class V(tuple):
    def __sub__(self, other):
        return V(a - b for a, b in zip(self, other))

    def dot(self, other):
        return sum(a * b for a, b in zip(self, other))


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, v1, v2, **data):
        self.edges.setdefault(v1, {})[v2] = data

    def copy(self):
        g = Graph()
        g.edges = deepcopy(self.edges)
        return g


def maximum_flow(g, source, sink):
    flow_g = g.copy()
    inf = 1 << 32

    def find_sink():
        q = []
        best = {}
        heapq.heappush(q, (-inf, source, []))
        while q:
            invcap, cur, path = heapq.heappop(q)
            cap = -invcap
            b = best.get(cur, 0)
            if cap < b:
                continue
            best[cur] = inf  # set to high to prevent further paths from being expanded
            if cur == sink:
                return reversed(path), cap

            path_here = path + [cur]
            for next, data in flow_g.edges.get(cur, {}).items():
                e_flow = data.get("flow", 0)
                e_cap = data.get("capacity", inf)
                free_cap = e_cap - e_flow
                next_flow = min(cap, free_cap)
                best_so_far = best.get(next, 0)
                if next_flow > best_so_far:
                    best[next] = next_flow
                    if next_flow > 0:
                        heapq.heappush(q, (
                            -next_flow,
                            next,
                            path_here
                        ))
        return None, 0

    tot_flow = 0
    while True:
        path, flow = find_sink()
        if flow == 0:
            break
        if flow == inf:
            return inf
        path = list(path)
        tot_flow += flow
        # add flow and residuals
        v2 = sink
        for v1 in path:
            data = flow_g.edges[v1][v2]
            data["flow"] = data.get("flow", 0) + flow
            rev_data = flow_g.edges.setdefault(v2, {}).setdefault(v1, {"capacity": 0})
            rev_data["flow"] = rev_data.get("flow", 0) - flow
            v2 = v1

    flows = []
    for u, vs in flow_g.edges.items():
        for v, data in vs.items():
            f = data.get("flow", 0)
            if f > 0:
                flows.append((u, v, f))

    return tot_flow, flows


#from networkx import Graph, maximum_flow_value
def solve(s, v, gophers, holes):
    maxdist2 = (v * s)**2
    graph = Graph()

    for gi, g in enumerate(gophers):
        for hi, h in enumerate(holes):
            dist2 = (h - g).dot(h - g)
            if dist2 <= maxdist2:
                graph.add_edge(f"g{gi}", f"h{hi}", capacity=1)

    for gi in range(len(gophers)):
        graph.add_edge("source", f"g{gi}", capacity=1)
    for hi in range(len(holes)):
        graph.add_edge(f"h{hi}", "sink", capacity=1)

    max_escape, _ = maximum_flow(graph, "source", "sink")
    print(len(gophers) - max_escape)


lines = [l.rstrip('\n') for l in sys.stdin.readlines()]
i = 0
while i < len(lines):
    n, m, s, v = [int(x) for x in lines[i].split(" ")]
    i += 1
    gophers = [V([float(x) for x in line.split(" ")]) for line in lines[i:i+n]]
    i += n
    holes = [V([float(x) for x in line.split(" ")]) for line in lines[i:i+m]]
    i += m
    solve(s, v, gophers, holes)

