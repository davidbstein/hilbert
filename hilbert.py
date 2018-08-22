#!/env/bin/eval python3

"""
hilbert curve 2d utils.

convert points (x, y) in a box with side length N to hilbert int d.

N must be a power of 2.
"""


def xy2d(n, x, y):
    """x, y on a box of side n to hilbert val d."""
    d = 0
    s = n // 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s ** 2 * ((3 * rx) ^ ry)
        x, y = _rot(s, x, y, rx, ry)
        s >>= 1
    return d


def d2xy(n, d):
    """Hilbert val d to x, y on a box of side n."""
    assert(d <= n**2 - 1)
    t = d
    x = y = 0
    s = 1
    while (s < n):
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        x, y = _rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def _rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y


def prettyprint(n):
    """Make a cool prettyprint."""
    output = [[None for _ in range(n)] for _ in range(n)]
    _pad = [
        "     ",
        "  |  ",
    ]
    _mid = [
        "  |  ",
        "--+  ",
        "  +--",
        "-----",
    ]
    _cache = {
        -1: (0, 0),
        n**2: (0, 0)
    }

    def md2xy(d):
        if not _cache.get(d):
            _cache[d] = d2xy(n, d)
        return _cache[d]

    for d in range(n**2):
        lst = md2xy(d - 1)
        cur = md2xy(d)
        nxt = md2xy(d + 1)
        output[cur[1]][cur[0]] = (
            _pad[(min(lst[1], nxt[1]) < cur[1])],
            _mid[
                0 +
                (min(lst[0], nxt[0]) < cur[0]) +
                2 * (max(lst[0], nxt[0]) > cur[0])
            ].format(d=d),
            _pad[(max(lst[1], nxt[1]) > cur[1])],
        )
    rowstrings = [
        "\n".join(''.join(subrow) for subrow in ziprow)
        for ziprow in
        [zip(*row) for row in output]
    ]
    print('\n'.join(rowstrings))


def test(n):
    """test."""
    for d in range(n**2):
        x, y = d2xy(n, d)
        assert d == xy2d(n, x, y), ""


if __name__ == "__main__":
    import sys
    prettyprint(2**int(sys.argv[1]))