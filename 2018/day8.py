from lib.input import aoc_input, ints

nums = ints(aoc_input())

def node(i):
    nodes, meta = nums[i:i+2]
    nxt = i+2
    metasum = 0

    sub_val = {}
    for ix in range(1, nodes + 1):
        nxt, ms, sv = node(nxt)
        sub_val[ix] = sv
        metasum += ms
    metasum += sum(nums[nxt:nxt+meta])

    if nodes:
        node_val = sum(sub_val.get(ix, 0) for ix in nums[nxt:nxt+meta])
    else:
        node_val = sum(nums[nxt:nxt+meta])

    return nxt + meta, metasum, node_val

_, metasum, val = node(0)

print(metasum)
print(val)