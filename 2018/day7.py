from heapq import heappush, heappop

from lib.input import aoc_input, lines, pb_input
import networkx as nx

instr = lines(aoc_input())

g = nx.DiGraph()

for l in instr:
    parts = l.split()
    a = parts[1]
    b = parts[7]
    g.add_edge(a, b)

node_order = ''.join(nx.lexicographical_topological_sort(g))
print(node_order)


def task_len(c):
    return 61 + ord(c) - ord('A')

done_times = {}
num_workers = 5
workers = [0] * num_workers
while len(done_times) < len(g.nodes):
    t = heappop(workers)
    for c in node_order:
        if c not in done_times and all(i in done_times for i, _ in g.in_edges(c)):
            deps_done_t = max((done_times[i] for i, _ in g.in_edges(c)), default=t)
            if deps_done_t <= t:
                done_times[c] = t + task_len(c)
                heappush(workers, done_times[c])
                break
    else:
        heappush(workers, min(s for s in done_times.values() if s > t))

print(max(done_times.values()))
