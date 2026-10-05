#!/usr/bin/env python3
"""
verify_folds.py - check which rectangular boxes a polyomino net folds into (grid folds only).

Standalone: Python 3 standard library only.

    python verify_folds.py                    # checks data/cells.txt against every box with the same surface area
    python verify_folds.py NETFILE [a,b,c ...] # a net "x,y;x,y;..." and optional boxes

A net FOLDS onto an a x b x c box when there is a placement of its unit squares on the box surface such that
  * every square lands on exactly one unit square of the surface (so the surface is covered exactly once), and
  * every pair of squares that share an edge in the flat net are glued along the corresponding edge on the box
    (folds happen only along grid lines; nothing inside the net is cut).
The check is exact integer arithmetic: positions are kept in doubled coordinates, so every value is an integer.
For every box that folds, the face each square lands on is written to folds.json (used by simulate_folding.py).
"""
import json, os, sys
from itertools import product

def box_surface(a, b, c):
    """Surface unit squares of [0,a]x[0,b]x[0,c] as (doubled centre, outward normal)."""
    D = (2 * a, 2 * b, 2 * c); out = []
    for ax in range(3):
        for sgn in (-1, 1):
            o1, o2 = [i for i in range(3) if i != ax]
            for u in range(1, D[o1], 2):
                for v in range(1, D[o2], 2):
                    p = [0, 0, 0]; p[ax] = D[ax] if sgn > 0 else 0; p[o1] = u; p[o2] = v
                    n = [0, 0, 0]; n[ax] = sgn
                    out.append((tuple(p), tuple(n)))
    return out, D

def add(p, q, k=1): return (p[0] + k * q[0], p[1] + k * q[1], p[2] + k * q[2])
def neg(v): return (-v[0], -v[1], -v[2])
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])

def step(state, d, D):
    """Move one square in plane direction d (0:+x 1:-x 2:+y 3:-y) on the box surface, rolling over edges."""
    p, n, ex, ey = state
    t = (ex, neg(ex), ey, neg(ey))[d]
    q = add(p, t, 2)
    if all(0 <= q[i] <= D[i] for i in range(3)):          # still on the same face
        return (q, n, ex, ey)
    # roll over the edge: the moving direction becomes the new normal, the old normal becomes the reverse of t
    q = add(add(p, t), neg(n))
    rot = lambda v: neg(n) if v == t else (n if v == neg(t) else v)
    return (q, t, rot(ex), rot(ey))

def folds(cells, dims):
    """Return {cell: (centre, normal, ex, ey)} for one valid folding, or None."""
    a, b, c = dims
    surf, D = box_surface(a, b, c)
    if len(surf) != len(cells): return None
    valid = {p for p, _ in surf}
    cellset = set(cells)
    xs = [x for x, _ in cells]; ys = [y for _, y in cells]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    root = min(cells)   # lexicographically first square: (57, -30), one end of the strip
    axes = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    nbr = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for (p0, n0), ex in product(surf, axes):
        if sum(ex[i] * n0[i] for i in range(3)) != 0: continue
        for m in (1, -1):
            ey = cross(n0, ex); ey = ey if m == 1 else neg(ey)
            st = {root: (p0, n0, ex, ey)}; used = {p0}; queue = [root]; ok = True
            while queue and ok:
                cur = queue.pop()
                for d, (dx, dy) in enumerate(nbr):
                    nb = (cur[0] + dx, cur[1] + dy)
                    if nb not in cellset: continue
                    s = step(st[cur], d, D)
                    if s[0] not in valid: ok = False; break
                    if nb in st:
                        if st[nb] != s: ok = False; break       # a net adjacency that is not glued on the box
                    else:
                        if s[0] in used: ok = False; break      # two squares on the same surface square
                        st[nb] = s; used.add(s[0]); queue.append(nb)
            if ok and len(st) == len(cells): return st
    return None

def boxes_of_area(A):
    N = A // 2
    return [(x, y, (N - x * y) // (x + y)) for x in range(1, N) for y in range(x, N)
            if 3 * x * x <= N and 2 * x * y + y * y <= N and (N - x * y) % (x + y) == 0] if A % 2 == 0 else []

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    netfile = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'data', 'cells.txt')
    line = next(l for l in open(netfile) if l.strip())          # first non-empty line
    cells = [tuple(map(int, t.split(','))) for t in line.strip().split(';') if t.strip()]
    cellset = set(cells)
    # shape checks: connected, no holes (Euler characteristic 1), no squares touching only at a corner
    seen = {cells[0]}; stack = [cells[0]]
    while stack:
        x, y = stack.pop()
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q in cellset and q not in seen: seen.add(q); stack.append(q)
    V = {(x + i, y + j) for x, y in cells for i in (0, 1) for j in (0, 1)}
    E = {e for x, y in cells for e in (((x, y), 'h'), ((x, y + 1), 'h'), ((x, y), 'v'), ((x + 1, y), 'v'))}
    def corner_only(vx, vy):   # the two squares on one diagonal of this vertex present, the other two absent
        sw, se, nw, ne = [(vx + i, vy + j) in cellset for i, j in ((-1, -1), (0, -1), (-1, 0), (0, 0))]
        return (sw and ne and not se and not nw) or (se and nw and not sw and not ne)
    pinch = sum(1 for v in V if corner_only(*v))
    print('net: %d squares, connected=%s, Euler characteristic=%d (1 = no holes), corner-only contacts=%d'
          % (len(cells), len(seen) == len(cells), len(V) - len(E) + len(cells), pinch))
    boxes = [tuple(map(int, s.split(','))) for s in sys.argv[2:]] or boxes_of_area(len(cells))
    result = {}
    for dims in boxes:
        st = folds(cells, dims)
        print('%-12s %s' % ('x'.join(map(str, dims)), 'FOLDS' if st else 'does not fold'), flush=True)
        if st:
            cx = (min(x for x, _ in cells) + max(x for x, _ in cells)) / 2; cy = (min(y for _, y in cells) + max(y for _, y in cells)) / 2
            root = min(cells)   # lexicographically first square: (57, -30), one end of the strip
            p0, n0, ex, ey = st[root]
            FACES = {(1, 0, 0): 0, (-1, 0, 0): 1, (0, 1, 0): 2, (0, -1, 0): 3, (0, 0, 1): 4, (0, 0, -1): 5}
            result['x'.join(map(str, dims))] = dict(
                box=list(dims), root=list(root), faceup=cross(ex, ey) == n0,
                face={'%d,%d' % q: FACES[s[1]] for q, s in st.items()})
    json.dump(result, open(os.path.join(here, 'folds.json'), 'w'))
    print('folds into %d box(es); face assignments written to folds.json' % len(result))

if __name__ == '__main__':
    main()
