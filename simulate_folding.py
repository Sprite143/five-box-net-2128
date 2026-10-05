#!/usr/bin/env python3
"""
simulate_folding.py - fold the net into each box as a rigid object, one fold line at a time, and test every
intermediate position for collisions (paper passing through paper). Needs numpy and scipy.

    python verify_folds.py              # first: writes folds.json (which face of the box each square lands on)
    python simulate_folding.py [BOX [ORDER [STEP [SHRINK]]]]
        BOX     e.g. 2x13x16 (default: every box in folds.json)
        ORDER   inout (default: fold lines nearest the middle of the strip first) or outin (farthest first)
        STEP    angle step in degrees (default 1)
        SHRINK  squares are shrunk about their centres by this factor for the collision test (default 0.99), so
                squares that legitimately share an edge or a corner do not count as colliding

Model. For a given box, the squares that land on the same face and are connected in the net form a flat, rigid
PANEL. Panels meet along straight hinge lines; for every box here the panels form a tree, so folding the hinge
lines one at a time is a genuine rigid motion of the whole paper: every panel stays flat and every pair of
neighbouring squares stays joined throughout. Each hinge turns from 0 to 90 degrees while all others are held fixed;
at every step the moving part is checked against the rest with an exact separating-axis test on the (shrunk) squares.
"""
import collections, json, os, sys, time
import numpy as np
from scipy.spatial import cKDTree

here = os.path.dirname(os.path.abspath(__file__))
line = next(l for l in open(os.path.join(here, 'data', 'cells.txt')) if l.strip())
cells = [tuple(map(int, t.split(','))) for t in line.strip().split(';') if t]
N = len(cells); idx = {c: i for i, c in enumerate(cells)}
allfolds = json.load(open(os.path.join(here, 'folds.json')))
order_kind = sys.argv[2] if len(sys.argv) > 2 else 'inout'
STEP = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
SHRINK = float(sys.argv[4]) if len(sys.argv) > 4 else 0.99
names = [sys.argv[1]] if len(sys.argv) > 1 else list(allfolds)

h = SHRINK / 2
loc = np.array([[[x - h, y - h, 0], [x + h, y - h, 0], [x + h, y + h, 0], [x - h, y + h, 0]] for x, y in cells], float)

def rot(axis, ang):
    x, y, z = axis / np.linalg.norm(axis); c, s = np.cos(ang), np.sin(ang); C = 1 - c
    return np.array([[c + x*x*C, x*y*C - z*s, x*z*C + y*s], [y*x*C + z*s, c + y*y*C, y*z*C - x*s], [z*x*C - y*s, z*y*C + x*s, c + z*z*C]])

def sat_hits(A, B):
    """A, B: (k,4,3) planar convex quads; True where they overlap (no separating axis)."""
    a1, a2 = A[:, 1] - A[:, 0], A[:, 3] - A[:, 0]; b1, b2 = B[:, 1] - B[:, 0], B[:, 3] - B[:, 0]
    na, nb = np.cross(a1, a2), np.cross(b1, b2)
    axes = [na, nb, np.cross(a1, b1), np.cross(a1, b2), np.cross(a2, b1), np.cross(a2, b2),
            np.cross(na, a1), np.cross(na, a2), np.cross(nb, b1), np.cross(nb, b2)]
    hit = np.ones(len(A), bool)
    for ax in axes:
        nrm = np.linalg.norm(ax, axis=1); ok = nrm > 1e-9
        u = np.where(ok[:, None], ax / np.maximum(nrm, 1e-12)[:, None], 0)
        pa = np.einsum('nkj,nj->nk', A, u); pb = np.einsum('nkj,nj->nk', B, u)
        hit &= ~(ok & ((pa.max(1) < pb.min(1) - 1e-9) | (pb.max(1) < pa.min(1) - 1e-9)))
    return hit

for name in names:
    fd = allfolds[name]
    face = [fd['face']['%d,%d' % c] for c in cells]; sign = 1.0 if fd['faceup'] else -1.0
    root = idx[tuple(fd['root'])]
    # panels = connected groups of squares on the same face
    comp = [-1] * N; panels = []
    for i in range(N):
        if comp[i] >= 0: continue
        k = len(panels); comp[i] = k; stack = [i]; members = [i]
        while stack:
            x, y = cells[stack.pop()]
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                j = idx.get(q)
                if j is not None and comp[j] < 0 and face[j] == face[i]: comp[j] = k; stack.append(j); members.append(j)
        panels.append(members)
    P = len(panels)
    adj = collections.defaultdict(list)            # panel -> [(other panel, square here, square there)]
    for i, (x, y) in enumerate(cells):
        for q in ((x + 1, y), (x, y + 1)):
            j = idx.get(q)
            if j is not None and comp[j] != comp[i]:
                adj[comp[i]].append((comp[j], i, j)); adj[comp[j]].append((comp[i], j, i))
    pairs = {tuple(sorted((a, b))) for a in adj for b, _, _ in adj[a]}
    assert len(pairs) == P - 1, 'panel graph is not a tree'
    # panel tree from the panel containing the root square; one hinge (representative square pair) per tree edge
    rp = comp[root]; porder = [rp]; ppar = {rp: None}; hinge = {}
    for a in porder:
        for b, i, j in adj[a]:
            if b not in ppar: ppar[b] = a; hinge[b] = (i, j); porder.append(b)
    children = collections.defaultdict(list)
    for b in porder[1:]: children[ppar[b]].append(b)
    def subtree_cells(b):
        out, todo = [], [b]
        while todo:
            q = todo.pop(); out += panels[q]; todo += children[q]
        return np.array(out)
    hinges = porder[1:] if order_kind == 'inout' else porder[1:][::-1]
    R = np.tile(np.eye(3), (N, 1, 1)); T = np.zeros((N, 3))
    t0 = time.time(); collisions = []; samples = 0
    for step_no, b in enumerate(hinges):
        i, j = hinge[b]                              # i in the parent panel, j in the child panel
        sub = subtree_cells(b); mask = np.zeros(N, bool); mask[sub] = True; rest = np.where(~mask)[0]
        dx, dy = cells[j][0] - cells[i][0], cells[j][1] - cells[i][1]
        mid = np.array([(cells[i][0] + cells[j][0]) / 2, (cells[i][1] + cells[j][1]) / 2, 0.])
        axis_w = R[i] @ np.array([-dy, dx, 0.]); pivot_w = R[i] @ mid + T[i]
        Wrest = np.einsum('nij,nkj->nki', R[rest], loc[rest]) + T[rest][:, None, :]
        tree = cKDTree(Wrest.mean(1))
        for k in range(1, int(round(90 / STEP)) + 1):
            M = rot(axis_w, sign * np.radians(k * STEP))
            Rs = np.einsum('ij,njk->nik', M, R[sub]); Ts = (T[sub] - pivot_w) @ M.T + pivot_w
            Wsub = np.einsum('nij,nkj->nki', Rs, loc[sub]) + Ts[:, None, :]
            near = tree.query_ball_point(Wsub.mean(1), r=SHRINK * 1.4143 + 1e-6)
            ia = [a for a, lst in enumerate(near) for _ in lst]; ib = [c for lst in near for c in lst]
            samples += 1
            if ia:
                hits = sat_hits(Wsub[ia], Wrest[ib])
                if hits.any():
                    w = np.where(hits)[0][0]
                    collisions.append((step_no + 1, k * STEP, cells[sub[ia[w]]], cells[rest[ib[w]]])); break
        M = rot(axis_w, sign * np.pi / 2)
        R[sub] = np.einsum('ij,njk->nik', M, R[sub]); T[sub] = (T[sub] - pivot_w) @ M.T + pivot_w
    W = np.einsum('nij,nkj->nki', R, loc) + T[:, None, :]
    distinct = len(set(map(tuple, np.round(W.mean(1) * 2).astype(int))))
    ext = sorted(round(float(v), 2) for v in (W.max((0, 1)) - W.min((0, 1)) + (1 - SHRINK)))
    print('box %s, order %s: %d panels, %d fold lines, %d positions checked, %d collisions; final: %d/%d squares on '
          'distinct spots, size %s (%.0fs)' % (name, order_kind, P, len(hinges), samples, len(collisions), distinct, N,
                                                ext, time.time() - t0))
    for col in collisions[:5]:
        print('   collision at fold line %d, %.0f degrees: square %s hits square %s' % col)
