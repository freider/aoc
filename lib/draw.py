import numpy as np
default_charmap = {
    0: " ",
    1: "█",
    2: "/",
    3: "o"
}


def sparse_to_array(coord_dict):
    pixel_coords = np.array([list(k) for k in coord_dict.keys()])

    # TODO: add normalization in case of negative coordinates or empty space
    offsets = pixel_coords.min(axis=0)

    dimensions = pixel_coords.max(axis=0) - offsets + 1

    arr = np.zeros(dimensions, dtype=int)
    for cord, col in coord_dict.items():
        arr[tuple(np.array(list(cord)) - offsets)] = col
    return arr


def draw(a, charmap=None):
    if charmap is None:
        charmap = default_charmap
    for row in a:
        rendered = ''.join(charmap[c] for c in row)
        print(rendered)
