import numpy as np

_SELECTION_BY_KIND = {
    "open": lambda z: z[0],
    "high": np.max,
    "low": np.min,
    "close": lambda z: z[-1],
}


def selection_process(Z, Y, kind):
    reduce = _SELECTION_BY_KIND[kind]
    Z = np.array(Z, dtype=float)
    for start, end in constant_runs(Y):
        Z[start : end + 1] = reduce(Z[start : end + 1])
    return Z


def constant_runs(Y):
    is_consts = Y[1:] == Y[:-1]
    const_start = None
    for i, is_const in enumerate(is_consts):
        if is_const and const_start is None:
            const_start = i
        elif not is_const and const_start is not None:
            yield const_start, i
            const_start = None
    if const_start is not None:
        yield const_start, len(Y) - 1


def excursion_size(Z, run):
    start, end = run
    return np.ptp(Z[start : end + 1])
