import heapq
from collections import deque
from copy import deepcopy

import sys

inf = 1 << 63


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


class CompactGraph:
    def __init__(self, size):
        self.size = size
        self.cap = [[0] * size for _ in range(size)]
        self.edges = [set() for _ in range(size)]

    def add_edge(self, v1, v2, cap=inf):
        # assert v1 not in self.edges[v2]
        self.edges[v1].add(v2)
        self.edges[v2].add(v1)
        self.cap[v1][v2] += cap


def maximum_flow_ford_fulkerson(g, source_id, sink_id):
    flows = [[0] * g.size for _ in range(g.size)]

    def find_sink():
        q = []
        best = [0] * g.size
        parent = [None] * g.size
        heapq.heappush(q, (-inf, source_id, None))
        while q:
            invflowhere, cur, parent_v = heapq.heappop(q)
            if parent[cur] is not None:
                continue
            parent[cur] = parent_v
            best[cur] = inf  # set high to prevent further equal paths from being added
            flow_here = -invflowhere
            if cur == sink_id:
                return parent, flow_here

            for next in g.edges[cur]:
                e_flow = flows[cur][next]
                e_cap = g.cap[cur][next]
                free_cap = e_cap - e_flow
                next_flow = min(flow_here, free_cap)

                if next_flow > best[next]:
                    best[next] = next_flow
                    heapq.heappush(q, (
                        -next_flow,
                        next,
                        cur
                    ))

        return None, 0

    tot_flow = 0
    while True:
        parent, flow = find_sink()
        if flow == 0:
            break

        tot_flow += flow
        # add flow and residuals
        v2 = sink_id
        v1 = parent[sink_id]
        while v2 != source_id:
            flows[v1][v2] += flow
            flows[v2][v1] -= flow
            v2 = v1
            v1 = parent[v1]
        assert v1 is None

        if flow == inf:
            tot_flow = inf
            break

    pos_flows = []
    for u, vs in enumerate(g.edges):
        for v in vs:
            if flows[u][v] > 0:
                pos_flows.append((u, v, flows[u][v]))

    return tot_flow, pos_flows


def maximum_flow(g, source_id, sink_id):
    flow = [[0] * g.size for _ in range(g.size)]

    def find_sink():
        levels = [-1] * g.size
        q = deque([(source_id)])
        levels[source_id] = 0

        while q:
            u = q.popleft()
            next_level = levels[u] + 1
            for v in g.edges[u]:
                if levels[v] == -1 and g.cap[u][v] > flow[u][v]:
                    levels[v] = next_level
                    q.append(v)

        return levels

    def send_flow(u, amount, levels):
        if u == sink_id:
            return amount
        tot_sent = 0
        for v in g.edges[u]:
            if levels[v] == levels[u] + 1:
                res = min(amount, g.cap[u][v] - flow[u][v])
                sent = send_flow(v, res, levels)
                amount -= sent
                tot_sent += sent
                flow[u][v] += sent
                flow[v][u] -= sent
        return tot_sent

    tot = 0
    while True:
        levels = find_sink()
        if levels[sink_id] == -1:
            break
        while True:
            sent = send_flow(source_id, inf, levels)

            if sent == 0:
                break

            tot += sent


    uvs = []
    for u in range(g.size):
        for v in g.edges[u]:
            if flow[u][v] > 0:
                uvs.append((u, v, flow[u][v]))

    return tot, uvs


lines = (l.strip() for l in sys.stdin.readlines())

n, m, s, t = [int(x) for x in next(lines).split(" ")]
g = CompactGraph(n)
for _ in range(m):
    u, v, c = [int(x) for x in next(lines).split(" ")]
    g.add_edge(u, v, cap=c)

tmp = maximum_flow(g, s, t)
f, uvs = tmp
print(n, f, len(uvs))
for u, v, f in uvs:
    print(u, v, f)
