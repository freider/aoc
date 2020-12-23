import heapq
from copy import deepcopy

import sys


class Graph:
    def __init__(self):
        self.edges = {}
        self.name_id_map = {}
        self.id_name_map = {}

    def _name_to_id(self, name):
        id = self.name_id_map.setdefault(name, len(self.name_id_map))
        self.id_name_map[id] = name
        return id

    def _id_to_name(self, id):
        return self.id_name_map[id]

    def add_edge(self, v1, v2, **data):
        self.edges.setdefault(self._name_to_id(v1), {})[self._name_to_id(v2)] = data

    def copy(self):
        g = Graph()
        g.edges = deepcopy(self.edges)
        g.name_id_map = deepcopy(self.name_id_map)
        return g


def maximum_flow(g, source, sink):
    source_id = g._name_to_id(source)
    sink_id = g._name_to_id(sink)
    flow_g = g.copy()
    inf = 1 << 32

    def find_sink():
        q = []
        best = {}
        heapq.heappush(q, (-inf, source_id, []))
        while q:
            invcap, cur, path = heapq.heappop(q)
            cap = -invcap
            b = best.get(cur, 0)
            if cap < b:
                continue
            best[cur] = inf  # set to high to prevent further paths from being expanded
            if cur == sink_id:
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

        if flow == inf:
            tot_flow = inf
            break

    flows = []
    for u, vs in flow_g.edges.items():
        for v, data in vs.items():
            f = data.get("flow", 0)
            if f > 0:
                flows.append((g._id_to_name(u), g._id_to_name(v), f))

    return tot_flow, flows


lines = [l.strip() for l in sys.stdin.readlines()]
while lines:
    n, m, s, t = [int(x) for x in lines[0].split(" ")]
    g = Graph()
    for e in lines[1:1+m]:
        u, v, c = [int(x) for x in e.split(" ")]
        g.add_edge(u, v, capacity=c)

    tmp = maximum_flow(g, s, t)
    f, uvs = tmp
    print(n, f, len(uvs))
    for u, v, f in uvs:
        print(u, v, f)
    lines = lines[1+m:]
