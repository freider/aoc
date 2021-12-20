import numpy as np
default_charmap = {
    0: " ",
    1: "█",
    2: "/",
    3: "o"
}


def sparse_to_array(coord_dict_or_sequence, translate=False):
    if isinstance(coord_dict_or_sequence, dict):
        coord_dict = coord_dict_or_sequence
    else:
        coord_dict = {coord: 1 for coord in coord_dict_or_sequence}

    pixel_coords = np.array([list(k) for k in coord_dict.keys()])

    if translate:
        offsets = pixel_coords.min(axis=0)
    else:
        offsets = np.zeros_like(pixel_coords[0])

    dimensions = pixel_coords.max(axis=0) - offsets + 1

    arr = np.zeros(dimensions, dtype=int)
    for cord, col in coord_dict.items():
        npcord = np.array(list(cord)) - offsets
        assert (npcord >= 0).all(), "Negative coordinates in sparse_to_array - use `translate=True` to translate"
        arr[tuple(npcord)] = col

    return arr


def draw(a, charmap=None):
    if charmap is None:
        charmap = default_charmap
    for row in a:
        rendered = ''.join(charmap[c] for c in row)
        print(rendered)
