import numpy as np

four_dir_2d = np.array([
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, 0),
])

eight_dir_2d = np.array(list({(y, x) for x in (-1, 0, 1) for y in (-1, 0, 1)} - {(0, 0)}))


def _neighboursx(arr2d, point2d, offsets):
    neighbours = offsets + point2d
    within_bounds = ((neighbours >= 0) & (neighbours < arr2d.shape)).all(axis=1)
    return neighbours[within_bounds]


def neighbours4(arr2d, point2d):
    return _neighboursx(arr2d, point2d, four_dir_2d)


def neighbours8(arr2d, point2d):
    return _neighboursx(arr2d, point2d, eight_dir_2d)


def coord_vals(arr2d, coord_arr):
    return arr2d[coord_arr[:, 0], coord_arr[:, 1]]
